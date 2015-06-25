#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @TODO: add license

"""
Sample file for Fabric settings.

Please copy this file to the production/ & staging/ folders
and modify as needed (the files will be be ignored by git).

$ cp sample.fabric.py production/fabric.py
"""


def get_settings(overrides={}):
    """Returns a dictionary with settings for Fabric.
    Allow to override some settings through a parameter.

    :param overrides: Dictionary with values for some options.
    """
    SETTINGS = {}

    # =========================================================================
    # SSH connections
    # =========================================================================
    # List of hosts to work on
    SETTINGS['hosts'] = ['example.com']
    # Username to log in in the remote machine
    SETTINGS['user'] = 'user'

    # =========================================================================
    # Database
    # =========================================================================
    SETTINGS['db_name'] = overrides.get('db_name', 'ctsi_dropper')

    # Name of the database that will be copied for feature testing deployment.
    # This database must exist and the database user must have
    # enough rights to dump it.
    SETTINGS['source_db'] = 'ctsi_dropper_s'

    # Database user used for create_db()
    SETTINGS['db_user'] = 'ctsi_dropper'

    # Password for db_user - included in settings, and ~user/.my.cnf if
    # you create that with mysql_conf().  If you don't enable the corresponding
    # option below, you will be prompted for a password.
    SETTINGS['db_password'] = 'SET_DB_PASSWORD_HERE'

    # Password for root DB user - included in ~user/.my.cnf if you create that
    # with mysql_conf().  If you don't enable the corresponding option below,
    # you will be prompted for a password for database creation (only).
    SETTINGS['db_root_password'] = 'SET_ROOT_DB_PASSWORD_HERE'

    # Command option for DB password.  The default ('-p') option will prompt
    # you for the password.  The alternate ('' - i.e. empty) can be used to
    # avoid password prompting, but only after you have run mysql_conf(), e.g.
    # `fab settings mysql_conf` to set up user's .my.cnf file.
    SETTINGS['db_password_opt'] = '-p'
    #SETTINGS['db_password_opt'] = ''

    # Command option for root DB password. The default ('-p') option will
    # prompt you for the password. The alternate
    # ('--defaults-group-suffix=_root') can be used to avoid password
    # prompting, but only after you have run mysql_conf(), e.g.
    # `fab settings mysql_conf` to set up user's .my.cnf file.
    SETTINGS['db_root_password_opt'] = '-p'
    #SETTINGS['db_root_password_opt'] = '--defaults-group-suffix=_root'

    # A meaningful name for the instance
    SETTINGS['project_name'] = overrides.get('project_name', 'dropper')
    # This URL will be used in the VirtualHost section
    SETTINGS['project_url'] = overrides.get('project_url',
                                            'dropper.example.com')
    # Change the prefix for the Apache apps paths
    SETTINGS['project_path'] = '/srv/apps/%(project_name)s' % SETTINGS
    SETTINGS['project_repo_path'] = '%(project_path)s/src' % SETTINGS
    SETTINGS['project_repo'] = overrides.get('project_repo',
        'git://github.com/ctsit/redi-dropper-client.git')

    # =========================================================================
    # Secret key
    # =========================================================================
    from base64 import b64encode
    from os import urandom
    SETTINGS['secret_key'] = b64encode(urandom(50))

    # =========================================================================
    # Virtualenv
    # =========================================================================
    # Python version that will be used in the virtualenv
    SETTINGS['python'] = 'python2.7'
    SETTINGS['env_path'] = '%(project_path)s/env' % SETTINGS

    # =========================================================================
    # Apache + VirtualHost + WSGI
    # =========================================================================
    # The group your web server is running on
    SETTINGS['server_group'] = 'www-data'
    SETTINGS['vhost_file'] = ('/etc/apache2/sites-available/%(project_name)s' %
                              SETTINGS)
    SETTINGS['wsgi_file'] = '%(project_path)s/deploy/dropper.wsgi' % SETTINGS

    return SETTINGS
