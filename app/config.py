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


class DefaultConfig(object):

    """ Default configuration data """
    LOG_LEVEL = logging.DEBUG

    # same folder as the config.py
    CONFIDENTIAL_SETTINGS_FILE = os.path.join(BASEDIR, 'deploy/settings.conf')

    # Use local or shib sso auth
    LOGIN_USING_SHIB_AUTH = True

    # REDCap project configs
    REDCAP_API_URL = ''
    REDCAP_API_TOKEN = ''
    REDCAP_DEMOGRAPHICS_FIELDS = ''

    # SSL Certificate config
    SERVER_SSL_KEY_FILE = '/etc/apache2/ssl/dropper.ctsi.ufl.edu.key'
    SERVER_SSL_CRT_FILE = '/etc/apache2/ssl/dropper.ctsi.ufl.edu.crt'

    # @see http://flask.pocoo.org/docs/0.10/config/
    # (!) Try changing this value to the real server name
    # if you keep getting back "GET / HTTP/1.1" 404 -
    SERVER_NAME = 'localhost:5000'

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

    from base64 import b64encode
    from os import urandom
    random_key = b64encode(urandom(50))
    SECRET_KEY = os.getenv('SECRET_KEY', random_key)
    # Limit the max upload size for the app to 20 MB
    # @see https://pythonhosted.org/Flask-Uploads/
    DEFAULT_MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    MAX_CONTENT_LENGTH = os.getenv(
        'REDIDROPPER_MAX_CONTENT_LENGTH',
        DEFAULT_MAX_CONTENT_LENGTH)

    # THREADS_PER_PAGE = 8
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = ""

    # override as needed in CONFIDENTIAL_SETTINGS_FILE
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


class TestConfig(DefaultConfig):

    """ Configuration for running tests """
    TESTING = True
    CSRF_ENABLED = False

    if os.getenv('CONTINUOUS_INTEGRATION', '') > '':
        # resolve a path when runing with TravisCI
        CONFIDENTIAL_SETTINGS_FILE = \
            '~/build/ctsit/redi-dropper-client/app/deploy/settings.conf'
