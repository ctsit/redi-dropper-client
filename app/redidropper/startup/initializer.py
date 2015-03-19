

from flask_user import UserManager, SQLAlchemyAdapter
import logging


def do_init(app, db, extra_settings={}):
    """
    Initialize the app

    @see run.py
    """

    # Load content from  'redidropper/startup/settings.py' file
    app.config.from_object('redidropper.startup.settings')


    # load routes
    from redidropper.routes import pages
    from redidropper.routes import users

    # load models
    #from redidropper.models import user


