"""
Goal: Load settings, configure logging, load application routing

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

import os
import sys
import ssl
import pprint
import logging
from flask import request
from logging import Formatter
from config import LOG_LEVEL

DEFAULT_CONFIG = 'config.DefaultConfig'
REDIDROPPER_CONFIG = 'REDIDROPPER_CONFIG'

def configure_app_environ(app):
    """
    Read the extra configs such as db passwords.
    Note: Use Apache directive

        SetEnv REDIDROPPER_CONFIG xyz

    to specify the path to the file.

    @see http://stackoverflow.com/questions/9016504/apache-setenv-not-working-as-expected-with-mod-wsgi
    """
    # pprint.pprint(os.environ)
    app_config = request.environ[REDIDROPPER_CONFIG]

    if app_config is None or '' == app_config.strip():
        print("Got variable REDIDROPPER_CONFIG: {}".format(app_config))

        if os.access(app_config, os.R_OK):
            app.config.from_envvar(REDIDROPPER_CONFIG)
            app.logger.info("Loaded app config from: {}" .format(app_config))
            print get_config_summary(app)
        else:
            app.logger.error("The app config file: {} is not readable. "
                             "Using default config only is unsafe."
                             .format(app_config))
            sys.exit()
    else:
        app.logger.error("""
        The `REDIDROPPER_CONFIG` environment variable is not set.
        Please create a config file with appropriate values and set the
        `REDIDROPPER_CONFIG` environment variable.

        Example:

            $ mkdir ~/.redidropper
            $ cp deploy/application.conf.sample ~/.redidropper/application.conf
            $ export REDIDROPPER_CONFIG=~/.redidropper/application.conf
        """)
        sys.exit()


def configure_app(app):
    """ Read the extra configs such as db passwords. """
    app_config = app.config[REDIDROPPER_CONFIG]

    if app_config is None or '' == app_config.strip():
        app.logger.error("The default config should specify the: {} file. "
                .format(REDIDROPPER_CONFIG))
        sys.exit()

    if os.access(app_config, os.R_OK):
        app.config.from_pyfile(app_config)
        app.logger.info("Loaded app config from: {}" .format(app_config))
    else:
        app.logger.error("The app config file: [{}] is not readable. "
                .format(app_config))
        sys.exit()


def do_init(app, db, extra_settings={}):
    """
    Initialize the app.

    @TODO: remove the `db` paramter if not used
    @see run.py

    :rtype Flask
    :return the initialized application object
    """
    app.config.from_object(DEFAULT_CONFIG)
    configure_logging(app, LOG_LEVEL)
    app.logger.info("Loaded default config from: {}".format(DEFAULT_CONFIG))
    print(get_config_summary(app))

    # Override with values stored in `REDIDROPPER_CONFIG` file
    configure_app(app)

    if len(extra_settings):
        # Override with special settings (example: tests/conftest.py)
        app.logger.info("Load extra config params using do_init()")
        app.config.update(extra_settings)

    # load routes
    from redidropper.routes import pages
    from redidropper.routes import users
    from redidropper.routes import api

    # print app.url_map
    print(get_config_summary(app))

    if not app.testing:
        # When runing tests there is no need for the debugtoolbar
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)
    return app


def configure_logging(app, debug_level):
    """
    Set the log location and formatting
    @see http://flask.pocoo.org/docs/0.10/errorhandling/
    """
    handler = logging.StreamHandler()
    fmt = Formatter('%(asctime)s %(levelname)s: '
                    '%(message)s [%(filename)s +%(lineno)d]')
    handler.setFormatter(fmt)
    handler.setLevel(debug_level)
    print("configure_logging() set debug level to: {}".format(debug_level))
    app.logger.addHandler(handler)


def get_config_summary(app):
    """ Helper method for debugging configuration """
    data = {
        "Debug mode": app.debug,
        "Secret key length": len(app.config['SECRET_KEY']),
        "Database host/db": "{}/{}"
        .format(app.config['DB_HOST'], app.config['DB_NAME']),
    }
    return data


def get_ssl_context(app):
    """
    Get a SSL context in debug mode
    @see http://werkzeug.pocoo.org/docs/0.10/serving/#quickstart
    """
    ssl_public_key_file = app.config['SERVER_SSL_CRT_FILE']
    ssl_private_key_file = app.config['SERVER_SSL_KEY_FILE']
    ssl_context = None

    if os.path.isfile(ssl_public_key_file) and \
            os.path.isfile(ssl_private_key_file):
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.load_cert_chain(ssl_public_key_file,
                                        ssl_private_key_file)
            print('Using ssl certificate {}'
                    .format(ssl_public_key_file))
        except Exception as exc:
            print("Problem loading SSL certificate: {}".format(exc))
    else:
        print("Could not read ssl cert/key: \n\t{}\n\t{}"
                .format(ssl_public_key_file, ssl_private_key_file))

        if app.debug:
            # if the pyOpenSSL is installed use the adhoc ssl context
            ssl_context = 'adhoc'
            print("Attempting to use the adhoc ssl_context")

    return ssl_context
