

from flask_user import UserManager, SQLAlchemyAdapter
import logging


def do_init(app, db, extra_settings={}):
    """
    Initialize the app

    @see run.py
    """

    # Load content from  'redidropper/startup/settings.py' file
    app.config.from_object('redidropper.startup.settings')

    UPLOAD_FOLDER = '/Users/sanathkumarpasumarthy/git' 
    TEMP_FOLDER = '/Users/sanathkumarpasumarthy/git/temp'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TEMP_FOLDER'] = TEMP_FOLDER

    # load routes
    from redidropper.routes import pages
    from redidropper.routes import users
    from redidropper.routes import api

    # load models
    #from redidropper.models import user


