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
# import sys
from os.path import isfile, join, abspath
# from os.path import isdir
# from pprint import pprint

from fabric.api import cd, env
from fabric.context_managers import hide, prefix, settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, upload_template
from fabric.operations import require, run, sudo
# from fabric.operations import get, put
from fabric.utils import abort


# =========================================================================
# Deployment repos
# =========================================================================

def load_environ(target, new_settings={}):
    """ Helper for loading an 'environ/fabric.py' file"""
    # pprint(sys.path)
    fab_conf_file = join(target, 'fabric.py')
    if not isfile(fab_conf_file):
        abort("Please create the '{}' file".format(fab_conf_file))

    try:
        fabric = imp.load_source('fabric', fab_conf_file)
    except ImportError:
        abort("Can't load '{}' environ; is PYTHONPATH exported?".format(target))

    env.update(fabric.get_settings(new_settings))
    env.environment = target


def production(new_settings={}):
    """Work on the production environment"""
    load_environ('production')


def staging(new_settings={}):
    """Work on the staging environment"""
    load_environ('staging')


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
    # Note: this is not affecting the "project_repo_path" used for "git clone"
    print('\n\nCreating initial directories...')

    _remove_directories()

    sudo('mkdir -p %(project_path)s' % env)
    sudo('mkdir -p %(project_path)s/uploaded_files' % env)
    sudo('mkdir -p %(project_path)s/logs' % env)
    # sudo('do something as user', user=notme)
    sudo('chown -R %(user)s:%(server_group)s %(project_path)s' % env)


def _init_virtualenv():
    """Creates initial virtualenv"""
    print('\n\nCreating virtualenv...')

    run('virtualenv -p %(python)s --no-site-packages %(env_path)s' % env)
    with prefix('source %(env_path)s/bin/activate' % env):
        run('easy_install pip')


def _clone_repo():
    """Clones the Git repository"""
    print('\n\nCloning the repository...')

    run('git clone %(project_repo)s %(project_repo_path)s' % env)


def _checkout_repo(branch="master"):
    """Updates the Git repository and checks out the specified branch"""
    print('\n\nUpdating repository branch...')
    print('\t Branch: {}'.format(branch))
    print('\t CWD: {}'.format(env.project_repo_path))

    with cd(env.project_repo_path):
        run('git checkout master')
        run('git pull')
        run('git checkout %s' % branch)

    run('chmod -R go=u,go-w %(project_repo_path)s' % env)


def _install_requirements():
    """Installs dependencies defined in the requirements file"""
    print('\n\nInstalling requirements...')

    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -r %(project_repo_path)s/app/requirements/deploy.txt' % env)
        run('chmod -R go=u,go-w %(env_path)s' % env)


def _update_requirements():
    """Updates dependencies defined in the requirements file"""
    print('\n\nUpdating requirements...')

    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -U -r %(project_repo_path)s/app/requirements/deploy.txt' % env)
        run('chmod -R go=u,go-w %(env_path)s' % env)


def is_prod():
    """Shortcut for env.environment == 'production'"""
    require('environment', provided_by=[production, staging])
    return env.environment == 'production'


def motd():
    """Print the message of the day"""
    print(MOTD_PROD if is_prod() else MOTD_STAG)


def bootstrap(branch="master"):
    """Bootstraps the deployment using the specified branch"""
    require('environment', provided_by=[production, staging])
    motd()

    if (not exists('%(project_path)s' % env) or
        confirm('\n%(project_path)s already exists. Do you want to continue?'
                % env, default=False)):
            with settings(hide('stdout', 'stderr')):
                _init_directories()
                _init_virtualenv()
                _clone_repo()
                _checkout_repo(branch=branch)
                _install_requirements()
    else:
        abort('\nAborting.')


def create_db():
    """Creates a new DB"""
    require('environment', provided_by=[production, staging])

    create_db_cmd = ("CREATE DATABASE `%(db_name)s` "
                     "DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
                     % env)
    grant_db_cmd = ("GRANT ALL PRIVILEGES ON `%(db_name)s`.* TO `%(db_user)s`"
                    "@localhost IDENTIFIED BY \"%(db_password)s\"; "
                    "FLUSH PRIVILEGES;"
                    % env)

    print('\n\nCreating DB...')

    with settings(hide('stderr')):
        run(("mysql -u %(db_user)s %(db_password_opt)s -e '" % env) +
            create_db_cmd +
            ("' || { test root = '%(db_user)s' && exit $?; " % env) +
            "echo 'Trying again, with MySQL root DB user'; " +
            ("mysql -u root %(db_root_password_opt)s -e '" % env) +
            create_db_cmd + grant_db_cmd + "';}")


def drop_db():
    """Drops the current DB - losing all data!"""
    require('environment', provided_by=[production, staging])

    print('\n\nDropping DB...')

    if confirm('\nDropping the %s DB loses ALL its data! Are you sure?'
               % (env['db_name']), default=False):
        run("echo 'DROP DATABASE `%s`' | mysql -u %s %s" %
            (env['db_name'], env['db_user'], env['db_password_opt']))
    else:
        abort('\nAborting.')


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

        local_file_wsgi = abspath('dropper.wsgi')  # same file for prod/ stag
        local_file_vhost = abspath('%(environment)s/virtualhost.conf' % env)
        local_file_settings = abspath('%(environment)s/settings.conf' % env)

        # Create a map of files to upload:
        #   local_file ==> remote_file
        files_map = {
            local_file_wsgi: env.wsgi_file,
            local_file_vhost: env.vhost_file,
            local_file_settings: env.settings_file,
        }

        # print files_map

        for local in files_map.keys():
            if not isfile(local):
                abort("Please create the file: {}".format(local))

            print('\nUploading {} \n to ==> {}'.format(local, files_map[local]))

            # @TODO: check if we still need to execute: chmod -R g=r,o-rwx
            upload_template(filename=local,
                            destination=files_map[local],
                            context=env,
                            use_sudo=True,
                            mirror_local_mode=False,
                            mode=None,  # 640
                            pty=None)


def install_site():
    """Configures the server and enables the site"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        update_config()  # upload new config files
        # check_syntax_apache()
        enable_site()  # execute a2ensite


def deploy(branch="master"):
    """Updates the code and installs the production site"""
    require('environment', provided_by=[production, staging])

    with settings(hide('stdout', 'stderr')):
        update_code(branch=branch)
        install_site()


def touch():
    """Reloads daemon processes by touching the WSGI file"""
    require('environment', provided_by=[production, staging])

    print('\n\nRunning `touch`...')

    with settings(hide('stdout', 'stderr')):
        run('touch %(wsgi_file)s' % env)


def mysql_conf():
    """Sets up .my.cnf file for passwordless MySQL operation"""
    require('environment', provided_by=[production, staging])

    print('\n\nSetting up MySQL password configuration...')

    conf_filename = '~/.my.cnf'

    if (not exists(conf_filename) or
        confirm('\n%s already exists. Do you want to overwrite it?'
                % conf_filename, default=False)):

        with settings(hide('stdout', 'stderr')):
            upload_template('deploy/my.cnf', conf_filename, context=env)
            run('chmod 600 %s' % conf_filename)

    else:
        abort('\nAborting.')


MOTD_PROD = """
 ____                                           __    ____  ____   ___  ____
|  _ \ _ __ ___  _ __  _ __   ___ _ __          \ \  |  _ \|  _ \ / _ \|  _ \
| | | | '__/ _ \| '_ \| '_ \ / _ \ '__|  _____   \ \ | |_) | |_) | | | | | | |
| |_| | | | (_) | |_) | |_) |  __/ |    |_____|  / / |  __/|  _ <| |_| | |_| |
|____/|_|  \___/| .__/| .__/ \___|_|            /_/  |_|   |_| \_\\___/|____/
                 |_|   |_|
"""

MOTD_STAG = """
 ____                                           __    ____ _____  _    ____
|  _ \ _ __ ___  _ __  _ __   ___ _ __          \ \  / ___|_   _|/ \  / ___|
| | | | '__/ _ \| '_ \| '_ \ / _ \ '__|  _____   \ \ \___ \ | | / _ \| |  _
| |_| | | | (_) | |_) | |_) |  __/ |    |_____|  / /  ___) || |/ ___ \ |_| |
|____/|_|  \___/| .__/| .__/ \___|_|            /_/  |____/ |_/_/   \_\____|
                 |_|   |_|
"""
