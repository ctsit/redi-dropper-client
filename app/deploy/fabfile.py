#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @TODO: add license

"""
Fabric deployment file.
@see
    http://fabric-docs.readthedocs.org/en/latest/
    http://docs.fabfile.org/en/latest/usage/fab.html#cmdoption--show
    http://docs.fabfile.org/en/latest/api/core/operations.html
"""

import imp
import sys
import os.path
from fabric import colors
from fabric.api import cd, env, local, lcd
from fabric.context_managers import hide, prefix, settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, upload_template
from fabric.operations import require, run, sudo
from fabric.utils import abort
# from pprint import pprint


def help():
    local('fab --list')


# =========================================================================
# Deployment repos
# =========================================================================

def load_environ(target, new_settings={}):
    """ Helper for loading an 'environ/fabric.py' file"""
    # pprint(sys.path)
    fab_conf_file = os.path.join(target, 'fabric.py')
    if not os.path.isfile(fab_conf_file):
        abort("Please create the '{}' file".format(fab_conf_file))

    try:
        fabric = imp.load_source('fabric', fab_conf_file)
    except ImportError:
        abort("Can't load '{}' environ; is PYTHONPATH exported?".format(target))

    env.update(fabric.get_settings(new_settings))
    env.environment = target


def production(new_settings={}):
    """Work on the production environment"""
    load_environ('production', new_settings)


def staging(new_settings={}):
    """Work on the staging environment"""
    load_environ('staging', new_settings)


def _remove_directories():
    """Removes initial directories"""
    # Note: this is not affecting the "project_repo_path" used for "git clone"
    print('\n\nRemoving directories...')

    if exists('%(project_path)s' % env):
        sudo('rm -rf %(project_path)s' % env)
    else:
        print('Path %(project_path)s does not exist' % env)


def _init_directories():
    """Creates initial directories"""
    # @TODO: create a backup if directory exists
    print('\n\nCreating initial directories...')
    _remove_directories()

    sudo('mkdir -p %(project_path)s/logs' % env)
    # sudo('do something as user', user=notme)
    sudo('chown -R %(user)s:%(server_group)s %(project_path)s' % env)

    # Let group members to delete files
    sudo('chmod -R 770 %(project_path)s' % env)


def _fix_perms(folder):
    """ Fixes permissions for a specified folder:
        $ chgrp authorized-group some-folder
        $ chmod -R g+w,o-rwx some-folder
    """
    run('chgrp -R {} {}'.format(env.server_group, folder))
    run('chmod -R g+sw,o-rwx {}'.format(folder))


def _init_virtualenv():
    """Creates initial virtualenv"""
    print('\n\nCreating virtualenv...')
    run('virtualenv -p %(python)s --no-site-packages %(env_path)s' % env)
    with prefix('source %(env_path)s/bin/activate' % env):
        run('easy_install pip')

    _fix_perms(env.env_path)


def _clone_repo():
    """Clones the Git repository"""
    print('\n\nCloning the repository...')
    run('git clone %(project_repo)s %(project_repo_path)s' % env)
    _fix_perms(env.project_repo_path)


def _checkout_repo(branch="master"):
    """Updates the Git repository and checks out the specified branch"""
    print('\n\nUpdating repository to branch [{}]...'.format(branch))
    print('\t CWD: {}'.format(env.project_repo_path))

    with cd(env.project_repo_path):
        # run('git checkout master')
        run('git fetch')
        run('git checkout -f %s' % branch)

    _fix_perms(env.project_repo_path)


def _install_requirements():
    """Installs dependencies defined in the requirements file"""
    print('\n\nInstalling requirements...')

    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -r %(project_repo_path)s/app/requirements/deploy.txt'
            % env)

    _fix_perms(env.env_path)


def _update_requirements():
    """Updates dependencies defined in the requirements file"""
    print('\n\nUpdating requirements...')

    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -U '
            ' -r %(project_repo_path)s/app/requirements/deploy.txt' % env)

    _fix_perms(env.env_path)


def _is_prod():
    """Shortcut for env.environment == 'production'"""
    require('environment', provided_by=[production, staging])
    return env.environment == 'production'


def _motd():
    """Print the message of the day"""
    print(MOTD_PROD if _is_prod() else MOTD_STAG)


def bootstrap(branch="master"):
    """Bootstraps the deployment using the specified branch"""
    require('environment', provided_by=[production, staging])
    _motd()

    msg = colors.red('\n%(project_path)s exists. '
                     'Do you want to continue anyway?' % env)

    if (not exists('%(project_path)s' % env)
            or confirm(msg, default=False)):
        with settings(hide('stdout', 'stderr')):
            _init_directories()
            _init_virtualenv()
            _clone_repo()
            _checkout_repo(branch=branch)
            # after we get the requirements files we install them
            _install_requirements()
    else:
        sys.exit('\nAborting.')


def mysql_conf():
    """ Helper task for storing mysql login credentials to the encrypted file
    ~/.mylogin.cnf

    Once created you can connect to the database without typing the password.
    Example:
        $ mysql_config_editor set --login-path=local --user=root --password \
            --host=localhost
        $ mysql --login-path=local


    For more details see:
        https://dev.mysql.com/doc/refman/5.6/en/mysql-config-editor.html
    """
    require('environment', provided_by=[production, staging])
    print("Storing the database credentials to ~/.mylogin.cnf")
    print(colors.yellow("⚠ Plese note that if you have a '#' in your password"
                        " then you have to specify the password in quotes."))
    cmd = ("mysql_config_editor set "
           " --login-path=fabric_%(db_host)s "
           " --user=%(db_user)s "
           " --password "
           " --host=%(db_host)s"
           % env)
    local(cmd, capture=True)


def mysql_login_path():
    require('environment', provided_by=[production, staging])
    return "fabric_%(db_host)s" % env


def mysql_conf_test():
    """ Check if a configuration was created for the host"""
    require('environment', provided_by=[production, staging])

    from subprocess import Popen, PIPE
    login_path = mysql_login_path()
    cmd = ("mysql_config_editor print --login-path={} 2> /dev/null"
           .format(login_path) % env)
    proc = Popen(cmd, shell=True, stdout=PIPE)
    (out, err) = proc.communicate()
    # print("Checking mysql login path: {}".format(login_path))
    has_config = ("" != out)

    if not has_config:
        print("There are no mysql credentials stored in ~/.mylogin.cnf file."
              " Please store the database credentials by running: \n\t"
              " fab {} mysql_conf".format(env.environment))
        sys.exit('\nAborting.')


def mysql_check_db_exists():
    """ Check if the specified database was already created """
    require('environment', provided_by=[production, staging])
    mysql_conf_test()

    cmd = ("echo 'SELECT COUNT(*) FROM information_schema.SCHEMATA "
           " WHERE SCHEMA_NAME = \"%(db_name)s\" ' "
           " | mysql --login-path=fabric_%(db_host)s "
           " | sort | head -1"
           % env)
    result = local(cmd, capture=True)
    # print("check_db_exists: {}".format(result))
    return result


def mysql_count_tables():
    """ Return the number of tables in the database """
    require('environment', provided_by=[production, staging])
    exists = mysql_check_db_exists()

    if not exists:
        abort(colors.red("Unable to list database '%(db_name)s' tables."
                         "The database does not exist." % env))

    login_path = mysql_login_path()
    cmd = ("echo 'SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES "
           " WHERE TABLE_SCHEMA = \"%(db_name)s\" ' "
           " | mysql --login-path={}"
           " | sort | head -1".format(login_path)
           % env)
    result = local(cmd, capture=True)
    return int(result)


def mysql_list_tables():
    """ Show the list of tables with row counts """
    require('environment', provided_by=[production, staging])
    exists = mysql_check_db_exists()

    if not exists:
        abort(colors.red("Unable to list database '%(db_name)s' tables."
                         "The database does not exist." % env))

    login_path = mysql_login_path()
    cmd = ("echo 'SELECT table_name, table_rows FROM INFORMATION_SCHEMA.TABLES "
           " WHERE TABLE_SCHEMA = \"%(db_name)s\" ' "
           " | mysql --login-path={}".format(login_path)
           % env)
    result = local(cmd, capture=True)
    print(result)


def mysql_create_tables():
    """ Create app tables.
    Assumes that the database was already created and
    an user was granted `create` privileges.
    """
    require('environment', provided_by=[production, staging])

    exists = mysql_check_db_exists()
    if not exists:
        abort(colors.red("Unable to create tables in database '%(db_name)s'."
                         "The database does not exist" % env))

    total_tables = mysql_count_tables()

    if total_tables > 0:
        print(colors.red("The database already contains {} tables."
                         .format(total_tables)))
        sys.exit("If you need to re-create the tables please run: "
                 "\n\t fab {} mysql_reset_tables"
                 .format(env.environment))

    login_path = mysql_login_path()
    files = ['001/upgrade.sql', '002/upgrade.sql', '002/data.sql']

    with lcd('../db/'):
        for sql in files:
            cmd = ("mysql --login-path={} %(db_name)s < {}"
                   .format(login_path, sql)
                   % env)
            local(cmd)


def mysql_drop_tables():
    """ Drop the app tables"""
    require('environment', provided_by=[production, staging])

    total_tables = mysql_count_tables()
    question = ("Do you want to drop the {} tables in '%(db_name)s'?"
                .format(total_tables) % env)
    if not confirm(question):
        abort(colors.yellow("Aborting at user request."))

    exists = mysql_check_db_exists()
    if not exists:
        abort(colors.red("Unable to drop tables in database '%(db_name)s'."
                         "The database does not exist" % env))

    files = ['002/downgrade.sql', '001/downgrade.sql']

    with lcd('../db/'):
        for sql in files:
            cmd = ("mysql --login-path=fabric_%(db_host)s %(db_name)s < {}"
                   .format(sql)
                   % env)
            local(cmd)


def mysql_reset_tables():
    total_tables = mysql_count_tables()

    if total_tables > 0:
        mysql_drop_tables()

    mysql_create_tables()


def _toggle_apache_site(state):
    """Switches site's status to enabled or disabled"""
    action = "Enabling" if state else "Disabling"
    print('\n%s site...' % action)
    env.apache_command = 'a2ensite' if state else 'a2dissite'
    sudo('%(apache_command)s %(project_name)s' % env)
    sudo('service apache2 reload')


def check_syntax_apache():
    """Check the syntax of apache configurations"""
    require('environment', provided_by=[production, staging])
    out = sudo('apache2ctl -S')
    print("\n ==> Apache syntax check: \n{}".format(out))


def show_errors_apache():
    """Show info about apache"""
    require('environment', provided_by=[production, staging])
    out = sudo('cat %(project_path)s/logs/error.log' % env)
    print("\n ==> Apache errors: \n{}".format(out))


def show_config_apache():
    """Show info about apache"""
    require('environment', provided_by=[production, staging])

    out = sudo('apachectl -V')
    print("\n ==> Apache config: \n{}".format(out))
    out = sudo('apachectl -S 2>&1')
    print("\n ==> Apache virtualhosts listening on port 443: \n{}".format(out))
    # sudo('apachectl -D DUMP_MODULES')


def enable_site():
    """Enables the site"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        _toggle_apache_site(True)


def disable_site():
    """Disables the site"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        _toggle_apache_site(False)


def update_code(branch="master"):
    """Updates the source code and its requirements"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        _checkout_repo(branch=branch)
        _update_requirements()
        _install_requirements()  # if we add new dependencies


def update_config():
    """Updates server configuration files"""

    """
    Warnings:
        - the CWD of the fabfile is used to specify paths
        - if you use the "%(var)s/ % env" syntax make *sure*
            that you provide the "var" in your fabric.py file
    """
    require('environment', provided_by=[production, staging])

    print('\n\nUpdating server configuration...')

    with settings(hide('stdout', 'stderr')):
        # Create a map of files to upload
        # https://github.com/fabric/fabric/blob/master/fabric/operations.py#put
        files_map = {
            0: {
                'local': os.path.abspath('dropper.wsgi'),
                'remote': env.wsgi_file,
                'mode': '644',
            },
            1: {
                'local': os.path.abspath('%(environment)s/virtualhost.conf'
                                         % env),
                'remote': env.vhost_file,
                'mode': '644',
                'group': 'root'
            },
            2: {
                'local': os.path.abspath('%(environment)s/settings.conf' % env),
                'remote': env.settings_file,
                'mode': '640'
            }
        }
        # print files_map

        for key, file_data in files_map.iteritems():
            local_file = file_data['local']
            remote_file = file_data['remote']
            mode = file_data['mode']

            if not os.path.isfile(local_file):
                abort("Please create the file: {}".format(local_file))

            print('\nUploading {} \n to ==> {} with mode {}'
                  .format(local_file, remote_file, mode))
            upload_template(filename=local_file,
                            destination=remote_file,
                            context=env,
                            use_sudo=True,
                            mirror_local_mode=False,
                            mode=mode,
                            pty=None)

            if 'group' in file_data:
                sudo('chgrp {} {}'.format(file_data['group'], remote_file))
                print("Changed group to {} for {}"
                      .format(file_data['group'], remote_file))
            else:
                sudo('chgrp {} {}'.format(env.server_group, remote_file))


def deploy(branch="master"):
    """Updates the code, config, requirements, and enables the site
    Note: you have to run the disable_site task before running this task
    """
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        update_code(branch=branch)
        update_config()  # upload new config files
        enable_site()  # execute a2ensite


def bootstrap_develop():
    """ Convenience method for calling: fab HOST bootstrap:develop"""
    bootstrap(branch='develop')


def deploy_develop():
    """ Convenience method for calling: fab HOST deploy:develop"""
    deploy(branch="develop")


def restart_wsgi_app():
    """Reloads daemon processes by touching the WSGI file"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        run('touch %(wsgi_file)s' % env)


def check_app():
    """cURLs the target server to check if the app is up"""
    require('environment', provided_by=[production, staging])
    local('curl -sk https://%(project_url)s | grep "Please login" ' % env)


def print_project_repo():
    print("%(project_repo)s" % env)


def print_project_name():
    print("%(project_name)s" % env)


def git_tags(url=None, last_only=False):
    """ Show repo tags"""
    require('environment', provided_by=[production, staging])

    if url is None:
        url = '%(project_repo)s' % env

    cmd = ('git ls-remote --tags {} '
           ' | cut -d / -f3 '
           ' | sort -t. -k 1,1n -k 2,2n -k 3,3n '.format(url))

    if last_only:
        cmd += ' | tail -1'
    result = local(cmd, capture=True)
    return result


def git_clone_tag(url=None, tag=None):
    """ Clone a `slim` version of the code """
    require('environment', provided_by=[production, staging])

    if url is None:
        url = '%(project_repo)s' % env
    if tag is None:
        tag = git_tags(url=url, last_only=True)

    destination = 'v{}'.format(tag)

    cmd = ('git clone -b {} --single-branch %(project_repo)s {}'
           .format(tag, destination) % env)

    local(cmd)


def git_archive_tag():
    """ Create a vTAG_NUMBER.tar archive file of the code
    suitable for deployment (excludes .git folder)

    Note: does not work with --remote=https://github.com/...)
    """
    require('environment', provided_by=[production, staging])
    last_tag = git_tags(last_only=True)
    archive_name = "v{}.tar".format(last_tag)

    local('git archive --format=tar --remote=. {} ../app > {}'
          .format(last_tag, archive_name))
    print("Created archive file: {}".format(archive_name))


# -----------------------------------------------------------------------------
MOTD_PROD = """
  ____                                        __    ____                _
 |  _ \ _ __ ___  _ __  _ __   ___ _ __   ____\ \  |  _ \ _ __ ___   __| |
 | | | | '__/ _ \| '_ \| '_ \ / _ \ '__| |_____\ \ | |_) | '__/ _ \ / _` |
 | |_| | | | (_) | |_) | |_) |  __/ |    |_____/ / |  __/| | | (_) | (_| |
 |____/|_|  \___/| .__/| .__/ \___|_|         /_/  |_|   |_|  \___/ \__,_|
                 |_|   |_|
"""

MOTD_STAG = """
  ____                                        __    ____
 |  _ \ _ __ ___  _ __  _ __   ___ _ __       \ \  |  _ \  _____   __
 | | | | '__/ _ \| '_ \| '_ \ / _ \ '__|  _____\ \ | | | |/ _ \ \ / /
 | |_| | | | (_) | |_) | |_) |  __/ |    |_____/ / | |_| |  __/\ V /
 |____/|_|  \___/| .__/| .__/ \___|_|         /_/  |____/ \___| \_/
                 |_|   |_|
"""
