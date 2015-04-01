# Goal: Store helper functions not tied to a specific module
#
# @authors:
#   Andrei Sura             <sura.andrei@gmail.com>
#   Ruchi Vivek Desai       <ruchivdesai@gmail.com>
#   Sanath Pasumarthy       <sanath@ufl.edu>
#

import logging
import html
from flask import flash


# @TODO: move to the configs
ALLOWED_EXTENSIONS = set([
        'txt', 'pdf',
        'png', 'jpg', 'jpeg', 'gif', 'tiff',
        'zip', 'tar', 'tgz', 'bz2'])

FLASH_CATEGORY_ERROR = 'error'
FLASH_CATEGORY_INFO = 'info'

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def flash_error(msg):
    flash(msg, FLASH_CATEGORY_ERROR)

def flash_info(msg):
    flash(msg, FLASH_CATEGORY_INFO)

def pack(msg_type, msg):
    """
    Create a string represenation of dictionary
        {'msg_type': 'msg'}
    """
    return '"{}": "{}"'.format(msg_type, html.escape(msg))

def pack_error(msg):
    return pack('error', msg)

def pack_info(msg):
    return pack('info', msg)
