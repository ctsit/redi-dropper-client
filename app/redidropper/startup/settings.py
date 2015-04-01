# Goal: Store settings which can be over-ruled
#       using environment variables.
#
# @authors:
#   Andrei Sura             <sura.andrei@gmail.com>
#   Ruchi Vivek Desai       <ruchivdesai@gmail.com>
#   Sanath Pasumarthy       <sanath@ufl.edu>
#
# @TODO: add code to check for valid paths
import os


# Limit the max upload size for the app to 20 MB
# @see https://pythonhosted.org/Flask-Uploads/
DEFAULT_MAX_CONTENT_LENGTH = 20 * 1024 * 1024
MAX_CONTENT_LENGTH = os.getenv('REDI_DROPPER_MAX_CONTENT_LENGTH', DEFAULT_MAX_CONTENT_LENGTH)

DB_USER = os.getenv('REDI_DROPPER_DB_USER', 'redidropper')
DB_PASS = os.getenv('REDI_DROPPER_DB_PASS', 'securepass')

# http://effbot.org/librarybook/os-path.htm
INCOMING_TEMP_DIR  = os.getenv('REDI_DROPPER_INCOMING_TEMP_DIR', \
        os.path.expanduser('~/.redidropper/incoming/temp'))

INCOMING_SAVED_DIR = os.getenv('REDI_DROPPER_NCOMING_SAVED_DIR',\
        os.path.expanduser('~/.redidropper/incoming/saved'))
