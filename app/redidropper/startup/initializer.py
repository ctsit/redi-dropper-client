# Goal: Init the application routes and read the settings
#
# @authors:
#   Andrei Sura             <sura.andrei@gmail.com>
#   Ruchi Vivek Desai       <ruchivdesai@gmail.com>
#   Sanath Pasumarthy       <sanath@ufl.edu>

from flask_user import UserManager, SQLAlchemyAdapter
import logging
from logging import Formatter

def do_init(app, db, extra_settings={}):
    """
    Initialize the app
    @see run.py
    """

    # Load content from  'redidropper/startup/settings.py' file
    app.config.from_object('redidropper.startup.settings')

    # Override with special settings (example: tests/conftest.py)
    app.config.update(extra_settings)

    # load routes
    from redidropper.routes import pages
    from redidropper.routes import users
    from redidropper.routes import api

    # load models
    #from redidropper.models import UserEntity
    #from redidropper.models import UserAuthEntity

    configure_logging(app)
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
        handler.setLevel(logging.DEBUG)

    app.logger.addHandler(handler)
