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


DB_USER = os.getenv('REDI_DROPPER_DB_USER', 'redidropper')
DB_PASS = os.getenv('REDI_DROPPER_DB_PASS', 'securepass')

# http://effbot.org/librarybook/os-path.htm
INCOMING_TEMP_DIR  = os.getenv('REDI_DROPPER_INCOMING_TEMP_DIR', \
        os.path.expanduser('~/.redidropper/incoming/temp'))

INCOMING_SAVED_DIR = os.getenv('REDI_DROPPER_NCOMING_SAVED_DIR',\
        os.path.expanduser('~/.redidropper/incoming/saved'))
