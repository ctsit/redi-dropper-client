"""
Goal: Store settings which can be over-ruled
       using environment variables.

@authors:
    Andrei Sura             <sura.andrei@gmail.com>
    Ruchi Vivek Desai       <ruchivdesai@gmail.com>
    Sanath Pasumarthy       <sanath@ufl.edu>
"""

import os

# Flask settings

SERVER_NAME = 'localhost:5000'

# @see http://flask.pocoo.org/docs/0.10/config/
DEBUG = False

# Set to True in order to view every redirect in the debug toolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

SECRET_KEY = os.getenv('SECRET_KEY', 'insecure_key')

# Limit the max upload size for the app to 20 MB
# @see https://pythonhosted.org/Flask-Uploads/
DEFAULT_MAX_CONTENT_LENGTH = 20 * 1024 * 1024
MAX_CONTENT_LENGTH = os.getenv('REDI_DROPPER_MAX_CONTENT_LENGTH', DEFAULT_MAX_CONTENT_LENGTH)

DB_USER = os.getenv('REDI_DROPPER_DB_USER', 'redidropper')
DB_PASS = os.getenv('REDI_DROPPER_DB_PASS', 'securepass')

# http://effbot.org/librarybook/os-path.htm
# @TODO: add code to check for valid paths
INCOMING_TEMP_DIR  = os.getenv('REDI_DROPPER_INCOMING_TEMP_DIR', \
        os.path.expanduser('~/.redidropper/temp'))

INCOMING_SAVED_DIR = os.getenv('REDI_DROPPER_NCOMING_SAVED_DIR',\
        os.path.expanduser('~/.redidropper/saved'))
