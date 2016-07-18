#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Goal: Implement simple tasks executed during deployment with deploy.sh
#
# @authors
#   Andrei Sura             <sura.andrei@gmail.com>
#   Taeber Rapczak          <taeber@ufl.edu>


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
from fabric.api import cd
from fabric.api import env, local, lcd
from fabric.context_managers import hide, prefix, settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, upload_template
from fabric.operations import require, sudo
from fabric.utils import abort
# from pprint import pprint


def help():
    local('fab --list')


# =========================================================================
# Deployment repos
# =========================================================================

def load_environ(target, new_settings={}):
    """ Load an environment properties file 'environ/fabric.py' """
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
    """Remove the top project directory"""
    print('\n\nRemoving directories...')

    if exists('%(project_path)s' % env):
        sudo('rm -rf %(project_path)s' % env)
    else:
        print('Path %(project_path)s does not exist' % env)


def _init_directories():
    """Create initial directories"""
    # @TODO: create a backup if directory exists
    print('\n\nCreating initial directories...')
    _remove_directories()

    sudo('mkdir -p %(project_path)s/logs' % env)
    # sudo('do something as user', user=notme)
    sudo('chown -R %(user)s:%(server_group)s %(project_path)s' % env)

    # Let group members to delete files
    sudo('chmod -R 770 %(project_path)s' % env)


def _fix_perms(folder):
    """ Fixe permissions for a specified folder:
        $ chgrp authorized-group some-folder
        $ chmod -R g+w,o-rwx some-folder
    """
    sudo('chgrp -R {} {}'.format(env.server_group, folder))
    sudo('chmod -R g+sw,o-rwx {}'.format(folder))


def _init_virtualenv():
    """Create initial virtualenv"""
    print('\n\nCreating virtualenv...')
    sudo('virtualenv -p %(python)s --no-site-packages %(env_path)s' % env,
         user=env.server_user)

    with prefix('source %(env_path)s/bin/activate' % env):
        sudo('easy_install pip', user=env.server_user)


def _install_requirements():
    """Install dependencies defined in the requirements file"""
    print('\n\nInstalling requirements...')

    with prefix('source %(env_path)s/bin/activate' % env):
        sudo('pip install -r '
             ' %(project_repo_path)s/app/requirements/deploy.txt' % env,
             user=env.server_user)


def _update_requirements():
    """Update dependencies defined in the requirements file"""
    print('\n\nUpdating requirements...')

    with prefix('source %(env_path)s/bin/activate' % env):
        sudo('pip install -U  -r '
             ' %(project_repo_path)s/app/requirements/deploy.txt' % env,
             user=env.server_user)


def _is_prod():
    """ Check if env.environment == 'production'"""
    require('environment', provided_by=[production, staging])
    return env.environment == 'production'


def bootstrap(tag='master'):
    """Bootstrap the deployment using the specified branch"""
    require('environment', provided_by=[production, staging])
    print(MOTD_PROD if _is_prod() else MOTD_STAG)
    msg = colors.red('\n%(project_path)s exists. '
                     'Do you want to continue anyway?' % env)

    if (not exists('%(project_path)s' % env)
            or confirm(msg, default=False)):
        with settings(hide('stdout', 'stderr')):
            _init_directories()
            _init_virtualenv()
            _git_clone_tag(tag=tag)
            _install_requirements()
            update_config(tag=tag)  # upload new config files
            enable_site()
    else:
        sys.exit('\nAborting.')


def deploy(tag='master'):
    """Update the code, config, requirements, and enable the site
    """
    require('environment', provided_by=[production, staging])
    print(MOTD_PROD if _is_prod() else MOTD_STAG)

    with settings(hide('stdout', 'stderr')):
        disable_site()
        _git_clone_tag(tag=tag)
        _install_requirements()
        _update_requirements()
        update_config(tag=tag)  # upload new config files
        enable_site()


def mysql_conf():
    """ Store mysql login credentials to the encrypted file
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


def _mysql_login_path():
    """ Create a string to be used for storing credentials to ~/.mylogin.cnf
    @see #mysql_conf()
    """
    require('environment', provided_by=[production, staging])
    return "fabric_%(db_host)s" % env


def mysql_conf_test():
    """ Check if a configuration was created for the host"""
    require('environment', provided_by=[production, staging])

    from subprocess import Popen, PIPE
    login_path = _mysql_login_path()
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

    login_path = _mysql_login_path()
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

    login_path = _mysql_login_path()
    cmd = ("echo 'SELECT table_name, table_rows FROM INFORMATION_SCHEMA.TABLES "
           " WHERE TABLE_SCHEMA = \"%(db_name)s\" ' "
           " | mysql --login-path={}".format(login_path)
           % env)
    result = local(cmd, capture=True)
    print(result)

def _is_valid_version(version_number):
    """Checks if the version has the right number of digits"""
    version_string = str(version_number)
    return len(version_string) <= 3

def _get_version_string(version_number):
    """Produces a three char string that corresponds to the desired db folder"""
    version_string = str(version_number)
    while len(version_string) < 3:
        version_string = '0' + version_string
    return version_string

def _step_to_version(version_number, is_upgrade):
    """Step once to the passed version. Must be on adjacent version
    Version numbers are given by the number for the folder
    in app/db/
    """
    require('environment', provided_by=[production, staging])

    exists = mysql_check_db_exists()
    if not exists:
        abort(colors.red("Unable to create tables in database '%(db_name)s'."
                         "The database does not exist" % env))
    if not _is_valid_version(version_number) is True:
        abort(colors.red("Unable to upgrade to version {} '%(db_name)s'."
                         "Please look in app/db for valid versions".format(version_number)
                         % env))

    login_path = _mysql_login_path()
    sql_file = 'upgrade.sql' if is_upgrade else 'downgrade.sql'
    sql = _get_version_string(version_number) + '/' + sql_file

    with lcd('../db/'):
        cmd = ("mysql --login-path={} %(db_name)s < {}"
                .format(login_path, sql)
                % env)
        local(cmd)

def mysql_version_upgrade(version_number):
    """Upgrade to the passed version. Must be on adjacent version
    Version numbers are given by the number for the folder
    in app/db/
    """
    _step_to_version(version_number, True)

def mysql_version_downgrade(version_number):
    """Downgrade to the passed version. Must be on adjacent version
    Version numbers are given by the number for the folder
    in app/db/
    """
    _step_to_version(version_number, False)

def mysql_create_tables():
    """ Create the application tables.
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

    login_path = _mysql_login_path()
    files = ['001/upgrade.sql',
             '002/upgrade.sql',
             '002/data.sql',
             '003/upgrade.sql',
             '004/upgrade.sql']

    with lcd('../db/'):
        for sql in files:
            cmd = ("mysql --login-path={} %(db_name)s < {}"
                   .format(login_path, sql)
                   % env)
            local(cmd)


def mysql_drop_tables():
    """ Drop the application tables"""
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

    files = ['004/downgrade.sql',
             '003/downgrade.sql',
             '002/downgrade.sql',
             '001/downgrade.sql']

    with lcd('../db/'):
        for sql in files:
            cmd = ("mysql --login-path=fabric_%(db_host)s %(db_name)s < {}"
                   .format(sql)
                   % env)
            local(cmd)


def mysql_reset_tables():
    """ Drop and re-create the application tables"""
    total_tables = mysql_count_tables()

    if total_tables > 0:
        mysql_drop_tables()

    mysql_create_tables()


def _toggle_apache_site(state):
    """Switch site's status to enabled or disabled
    Note: the `project_name` is used for referencing the config files
    """
    action = "Enabling" if state else "Disabling"
    print('\n%s site...' % action)
    env.apache_command = 'a2ensite' if state else 'a2dissite'
    sudo('%(apache_command)s %(project_name)s' % env)

    # We have to have the ssl config too because we use the NetScaler
    sudo('%(apache_command)s %(project_name)s-ssl' % env)
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
    """Enable the site"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        _toggle_apache_site(True)


def disable_site():
    """Disable the site"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        _toggle_apache_site(False)


def update_config(tag='master'):
    """Update server configuration files

    Warnings:
        - the CWD of the fabfile is used to specify paths
        - if you use the "%(var)s/ % env" syntax make *sure*
            that you provide the "var" in your fabric.py file
    """
    require('environment', provided_by=[production, staging])

    print('\n\nUpdating server configuration...')

    local_settings_file = os.path.abspath('%(environment)s/settings.conf' % env)
    local("""sed -i'.bak' -e "s|^APP_VERSION.*|APP_VERSION = '{}'|" {}"""
          .format(tag, local_settings_file))

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
                'local': os.path.abspath('%(environment)s/virtualhost-ssl.conf'
                                         % env),
                'remote': env.vhost_ssl_file,
                'mode': '644',
                'group': 'root'
            },
            3: {
                'local': local_settings_file,
                'remote': env.settings_file,
                'mode': '640'
            }
        }
        # print files_map

        # upload files but create a bakup with *.bak extension if the
        # remote file already exists
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


def restart_wsgi_app():
    """Reload the daemon processes by touching the WSGI file"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        sudo('touch %(wsgi_file)s' % env)


def check_app():
    """cURL the target server to check if the app is up"""
    require('environment', provided_by=[production, staging])
    local('curl -sk https://%(project_url)s | grep "Version " '
          ' | grep -oE "[0-9.]{1,2}[0-9.]{1,2}[0-9a-z.]{1,4}" | head -1 ' % env)


def print_project_repo():
    """ Show the git repository path specified in the fabric.py file"""
    print("\n Project repo: {}".format(env.project_repo))


def print_project_name():
    """ Show the project name uses as name for deploying the code"""
    print("Project name: {}".format(env.project_name))


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


def _git_clone_tag(tag=None):
    """ Clone a `slim` version of the code

    Note: if the tag was already deployed once we create a backup
    """
    require('environment', provided_by=[production, staging])

    url = env.project_repo
    if tag is None:
        print(colors.yellow(
            "No tag specified. Attempt to read the last tag from: {}"
            .format(url)))
        tag = git_tags(url=url, last_only=True)

    if not tag:
        abort(colors.red('\nPlease specify a valid tag.'))

    # Clone the code to src/v0.0.1`
    destination = ('%(project_path_src)s/v{}'.format(tag) % env)
    cmd = ('git clone -b {} --single-branch %(project_repo)s {}'
           .format(tag, destination) % env)

    if exists(destination):
        with cd(env.project_path_src):
            cmd_mv = 'mv v{} backup_`date "+%Y-%m-%d"`_v{}'.format(tag, tag)
            sudo(cmd_mv, user=env.server_user)

    sudo(cmd, user=env.server_user)
    _fix_perms(destination)

    with cd(env.project_path_src):
        # Create symlink
        sudo('ln -nsf {} current'.format(destination), user=env.server_user)


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
