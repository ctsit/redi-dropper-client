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
    SETTINGS['hosts'] = ['PLEASE_EDIT_ME']  # ['dropper1.ctsi.ufl.edu']
    # Username to log in in the remote machine
    SETTINGS['user'] = 'PLEASE_EDIT_ME'

    # =========================================================================
    # Database
    # =========================================================================
    SETTINGS['db_user'] = 'PLEASE_EDIT_ME'
    SETTINGS['db_pass'] = 'PLEASE_EDIT_ME'
    SETTINGS['db_host'] = 'PLEASE_EDIT_ME'
    SETTINGS['db_name'] = 'PLEASE_EDIT_ME'

    # =========================================================================
    # File storage
    # =========================================================================
    SETTINGS['redidropper_upload_temp_dir'] = 'PLEASE_EDIT_ME'  # '/ext/www/prod/mri_images_temp'
    SETTINGS['redidropper_upload_saved_dir'] = 'PLEASE_EDIT_ME'  # '/ext/www/prod/mri_images'

    # =========================================================================
    # REDCap
    # =========================================================================
    SETTINGS['redcap_api_url'] = 'https://redcap.example.com/redcap/api/'
    SETTINGS['redcap_api_token'] = 'PLEASE_EDIT_ME'  # 'the secret'
    SETTINGS['redcap_demographics_subject_id'] = 'PLEASE_EDIT_ME'  # 'ptid'

    # A meaningful name for the instance
    SETTINGS['project_name'] = 'PLEASE_EDIT_ME'  # 'dropper'
    # This URL will be used in the VirtualHost section
    SETTINGS['project_url'] = 'PLEASE_EDIT_ME'  # 'dropper.ctsi.ufl.edu'

    # Change the prefix for the Apache apps paths
    SETTINGS['project_path'] = '/srv/apps/%(project_name)s' % SETTINGS
    SETTINGS['project_path_src'] = '%(project_path)s/src' % SETTINGS
    SETTINGS['project_repo_path'] = '%(project_path)s/src/current' % SETTINGS
    SETTINGS['project_repo'] = 'git://github.com/ctsit/redi-dropper-client.git'

    # =========================================================================
    # Secret key (stored in settings.conf when we deploy)
    # =========================================================================
    from base64 import b64encode
    from os import urandom
    SETTINGS['secret_key'] = b64encode(urandom(50))

    # =========================================================================
    # Virtualenv
    # =========================================================================
    SETTINGS['python'] = 'python2.7'
    SETTINGS['env_path'] = '%(project_path)s/env' % SETTINGS

    # =========================================================================
    # Apache + VirtualHost + WSGI
    # =========================================================================
    # The user/group your web server is running on
    SETTINGS['server_user'] = 'PLEASE_EDIT_ME'  # 'www-data'
    SETTINGS['server_group'] = 'PLEASE_EDIT_ME'  # 'www-data'
    SETTINGS['vhost_file'] = ('/etc/apache2/sites-available/%(project_name)s' %
                              SETTINGS)
    SETTINGS['vhost_ssl_file'] = ('/etc/apache2/sites-available/%(project_name)s-ssl' %
                                  SETTINGS)
    SETTINGS['wsgi_file'] = ('%(project_path)s/dropper.wsgi' %
                             SETTINGS)
    SETTINGS['settings_file'] = ('%(project_path)s/settings.conf' %
                                 SETTINGS)

    return SETTINGS
