"""
Goal: Implement the default-config and test-config clases

@authors:
    Andrei Sura             <sura.andrei@gmail.com>
    Ruchi Vivek Desai       <ruchivdesai@gmail.com>
    Sanath Pasumarthy       <sanath@ufl.edu>
"""

import os
from datetime import timedelta
import logging

BASEDIR = os.path.abspath(os.path.dirname(__file__))

MODE_TEST = 'mode_test'     # for unit tests
MODE_PROD = 'mode_prod'     # for production
MODE_DEBUG = 'mode_debug'   # for developer mode


class DefaultConfig(object):

    """ Default configuration data """
    LOG_LEVEL = logging.DEBUG

    # When we deploy we use /srv/apps/dropper/ folder
    CONFIDENTIAL_SETTINGS_FILE = os.path.join(BASEDIR,
                                              '/srv/apps/dropper/settings.conf')

    # Use local or shib sso auth
    LOGIN_USING_SHIB_AUTH = True

    # REDCap project configs
    REDCAP_API_URL = ''
    REDCAP_API_TOKEN = ''
    REDCAP_DEMOGRAPHICS_SUBJECT_ID = ''

    # SSL Certificate config
    # Note: the paths to the certificate do *not matter* when the app is
    # served by Apache since Apache has its own configuration for that
    SERVER_SSL_KEY_FILE = 'ssl/server.key'
    SERVER_SSL_CRT_FILE = 'ssl/server.crt'

    # @see http://flask.pocoo.org/docs/0.10/config/
    #   `The name and port number of the server. Required for subdomain support
    #   (e.g.: 'myapp.dev:5000') Note that localhost does not support subdomains
    #   so setting this to `localhost` does not help. Setting a SERVER_NAME also
    #   by default enables URL generation without a request context but with an
    #   application context.`
    #
    # (!) Try changing or *removing* this value
    # if you keep getting back "GET / HTTP/1.1" 404 -
    # SERVER_NAME = 'debian-jessie:443'

    # the browser will not send a cookie with the secure flag set over an
    # unencrypted HTTP request
    SESSION_COOKIE_SECURE = True

    # https://www.owasp.org/index.php/Session_Management_Cheat_Sheet
    # flask.pocoo.org/docs/0.10/api/#flask.Flask.permanent_session_lifetime
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    DEBUG = False
    TESTING = False

    DEBUG_TB_ENABLED = False

    # Set to True in order to view every redirect in the debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # email config
    MAIL_SENDER_SUPPORT = os.getenv('REDIDROPPER_MAIL_SENDER_SUPPORT',
                                    'admin@example.com')
    MAIL_SERVER = os.getenv('REDIDROPPER_MAIL_SERVER',
                            'smtp.gmail.com')
    MAIL_PORT = os.getenv('REDIDROPPER_MAIL_PORT', 465)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('REDIDROPPER_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('REDIDROPPER_MAIL_PASSWORD')

    print MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
    # Database configuration is stored outside version control
    # in the `application.cfg` file
    DB_HOST = ''
    DB_NAME = ''

    # Limit the max upload size for the app to 20 MB
    # @see https://pythonhosted.org/Flask-Uploads/
    DEFAULT_MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    MAX_CONTENT_LENGTH = os.getenv(
        'REDIDROPPER_MAX_CONTENT_LENGTH',
        DEFAULT_MAX_CONTENT_LENGTH)

    # THREADS_PER_PAGE = 8
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = ""

    # override as needed in the settings file
    REDIDROPPER_UPLOAD_TEMP_DIR = os.getenv('REDIDROPPER_UPLOAD_TEMP_DIR',
                                            os.path.join(BASEDIR,
                                                         'upload/temp'))

    REDIDROPPER_UPLOAD_SAVED_DIR = os.getenv('REDIDROPPER_UPLOAD_SAVED_DIR',
                                             os.path.join(BASEDIR,
                                                          'upload/saved'))


class DebugConfig(DefaultConfig):

    """ Extra flag for debugging """
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # same folder as config.py
    CONFIDENTIAL_SETTINGS_FILE = os.path.join(BASEDIR,
                                              'deploy/settings.conf')


class TestConfig(DefaultConfig):

    """ Configuration for running tests """
    TESTING = True
    CSRF_ENABLED = False
    CONFIDENTIAL_SETTINGS_FILE = os.path.join(BASEDIR,
                                              'deploy/settings.conf')

    if os.getenv('CONTINUOUS_INTEGRATION', '') > '':
        print("CONTINUOUS_INTEGRATION: {}"
              .format(os.getenv('TRAVIS_BUILD_DIR')))
