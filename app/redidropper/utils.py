"""
Goal: Store helper functions not tied to a specific module

@authors:
    Andrei Sura             <sura.andrei@gmail.com>
    Ruchi Vivek Desai       <ruchivdesai@gmail.com>
    Sanath Pasumarthy       <sanath@ufl.edu>
"""

import json
from flask import flash

# @TODO: move to the configs
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff',
                          'zip', 'tar', 'tgz', 'bz2'])

FLASH_CATEGORY_ERROR = 'error'
FLASH_CATEGORY_INFO = 'info'


def clean_int(dangerous):
    """
    Return None for non-integer input
    Warning: do not use the
    """
    if dangerous is None:
        return None

    dangerous = str(dangerous).strip()

    if "" == dangerous:
        return None

    if not dangerous.isdigit():
        return None

    return int(dangerous)


def allowed_file(filename):
    """
    Checks if the specified file name should be allowed for downloading

    :rtype Boolean
    :return True if the filename is in the ALLOWED_EXTENSIONS whitelist
    """
    if filename is None:
        return False

    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def flash_error(msg):
    """ Put a message in the "error" queue for display """
    flash(msg, FLASH_CATEGORY_ERROR)


def flash_info(msg):
    """ Put a message in the "info" queue for display """
    flash(msg, FLASH_CATEGORY_INFO)


def pack(msg_type, msg):
    """
    Create a string represenation of dictionary
        {'msg_type': 'msg'}
    """
    return '{' + '"{}": {}'.format(msg_type, json.dumps(msg)) + '}'


def pack_error(msg):
    """ Format an error message to be json-friendly """
    return pack('error', msg)


def pack_info(msg):
    """ Format an info message to be json-friendly """
    return pack('info', msg)
