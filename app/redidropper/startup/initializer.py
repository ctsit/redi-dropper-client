"""
Goal: Load settings, configure logging, load application routing

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

import os
import sys
# import pprint
import logging
from logging import Formatter
from flask_debugtoolbar import DebugToolbarExtension
from redidropper.config import LOG_LEVEL

# DEFAULT_CONFIG = 'redidropper.startup.config'
DEFAULT_CONFIG = 'redidropper.config.DefaultConfig'
REDIDROPPER_CONFIG = 'REDIDROPPER_CONFIG'


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
    print get_config_summary(app)

    # Override with values stored in `REDIDROPPER_CONFIG` file
    #   cp startup/application.cfg.example startup/application.cfg
    #   export REDIDROPPER_CONFIG=
    #        ~/git/redi-dropper-client/app/redidropper/startup/application.cfg
    if REDIDROPPER_CONFIG in os.environ:
        app_config = os.environ[REDIDROPPER_CONFIG]

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
        app.logger.error("The `REDIROPPER_CONFIG` environment "
                         "variable is not set.")
        app.logger.info("Please create a config file and set the "
                        "environment variable appropriately.")
        sys.exit()

    if len(extra_settings):
        # Override with special settings (example: tests/conftest.py)
        app.logger.info("Load extra config params using do_init()")
        app.config.update(extra_settings)

    # configure_security(app, db)

    # load routes
    from redidropper.routes import pages
    from redidropper.routes import users
    from redidropper.routes import api

    if not app.testing:
        # When runing tests there is no need to for the debugtoolbar
        DebugToolbarExtension(app)
    return app


def configure_security(app, db):
    """ optional usage of security module """
    from flask_security import Security, SQLAlchemyUserDatastore
    from redidropper.models.user_entity import UserEntity
    from redidropper.models.role_entity import RoleEntity
    user_datastore = SQLAlchemyUserDatastore(db, UserEntity, RoleEntity)
    Security(app, user_datastore)
    app.logger.info("Loaded extension Flask-Security")


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
