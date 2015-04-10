"""
Goal: Init the application routes and read the settings

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

import os
import logging
from logging import Formatter
from flask_debugtoolbar import DebugToolbarExtension

DEFAULT_CONFIG = 'redidropper.startup.config'
REDIDROPPER_CONFIG = 'REDIDROPPER_CONFIG'

def do_init(app, db, extra_settings={}):
    """
    Initialize the app
    @see run.py
    """
    print("Load default config from object: {}".format(DEFAULT_CONFIG))
    app.config.from_object(DEFAULT_CONFIG)

    # Override with values stored in `REDIDROPPER_CONFIG` file
    #   cp startup/application.cfg.example startup/application.cfg
    #   export REDIDROPPER_CONFIG=~/git/redi-dropper-client/app/redidropper/startup/application.cfg
    app_config = os.environ[REDIDROPPER_CONFIG] if REDIDROPPER_CONFIG in os.environ else None

    if app_config:
        if os.access(app_config, os.R_OK):
            print("Loading application config from: {}" .format(app_config))
            app.config.from_envvar(REDIDROPPER_CONFIG)
        else:
            print('The specified config file: {} is not readable' \
                    .format(app_config))
    else:
        print("No `REDIROPPER_CONFIG` environment variable set. " \
                "Using the default: {}".format(DEFAULT_CONFIG))

    if len(extra_settings):
        # Override with special settings (example: tests/conftest.py)
        print("Load extra application using do_init()")
        app.config.update(extra_settings)

    # load routes
    from redidropper.routes import pages
    from redidropper.routes import users
    from redidropper.routes import api

    configure_logging(app)
    DebugToolbarExtension(app)
    return app


def configure_logging(app):
    """
    Set the log location and formatting
    @see http://flask.pocoo.org/docs/0.10/errorhandling/
    """
    handler = logging.StreamHandler()
    fmt = Formatter(
        '%(asctime)s %(levelname)s: %(message)s ' \
            '[in %(pathname)s:%(lineno)d]'
    )
    handler.setFormatter(fmt)
    if app.debug:
        print "Logging.setLevel(DEBUG)"
        handler.setLevel(logging.DEBUG)
    else:
        print "Logging.setLevel(INFO)"
        handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)
