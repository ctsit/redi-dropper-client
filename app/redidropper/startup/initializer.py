# Goal: Init the application routes and read the settings
#
# @authors:
#   Andrei Sura             <sura.andrei@gmail.com>
#   Ruchi Vivek Desai       <ruchivdesai@gmail.com>
#   Sanath Pasumarthy       <sanath@ufl.edu>

from flask_user import UserManager, SQLAlchemyAdapter
import logging


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
    #from redidropper.models import user

    return app
