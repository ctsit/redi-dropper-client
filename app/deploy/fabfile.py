#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @TODO: add license

"""
Fabric deployment file.
@see
    http://fabric-docs.readthedocs.org/en/latest/
"""

import imp
import sys
from os.path import isfile, isdir, join
#from pprint import pprint

from fabric.api import cd, env
from fabric.context_managers import hide, prefix, settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, upload_template
from fabric.operations import get, put, require, run, sudo
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
    if exists('%(project_path)s' % env):
        sudo('rm -rf %(project_path)s' % env)
    else:
        print('Path %(project_path)s doe not exist' % env)

    if exists('%(repos_path)s' % env):
        sudo('rm -rf %(repos_path)s' % env)
    else:
        print('Path %(repos_path)s doe not exist' % env)


def _init_directories():
    """Creates initial directories"""
    print('\n\nCreating initial directories...')

    _remove_directories()

    sudo('mkdir -p %(project_path)s' % env)
    sudo('mkdir -p %(project_path)s/logs' % env)
    sudo('mkdir -p %(repos_path)s' % env)
    sudo('chown -R %(user)s:%(server_group)s '
         '%(project_path)s %(repos_path)s' % env)


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

    with cd(env.project_repo_path):
        run('git checkout master')
        run('git pull')
        run('git checkout %s' % branch)
    run('chmod -R go=u,go-w %(project_repo_path)s' % env)


def _install_requirements():
    """Installs dependencies defined in the requirements file"""
    print('\n\nInstalling requirements...')

    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -r %(project_repo_path)s/requirements/deploy.txt' % env)
        run('chmod -R go=u,go-w %(env_path)s' % env)


def _update_requirements():
    """Updates dependencies defined in the requirements file"""
    print('\n\nUpdating requirements...')

    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -U -r %(project_repo_path)s/requirements/deploy.txt' % env)
        run('chmod -R go=u,go-w %(env_path)s' % env)


def bootstrap(branch="master"):
    """Bootstraps the deployment using the specified branch"""
    require('environment', provided_by=[production, staging])

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


def _toggle_apache_site(state):
    """Switches site's status to enabled or disabled"""
    action = "Enabling" if state else "Disabling"
    print('\n%s site...' % action)
    env.apache_command = 'a2ensite' if state else 'a2dissite'
    sudo('%(apache_command)s %(project_name)s' % env)
    sudo('service apache2 reload')

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

