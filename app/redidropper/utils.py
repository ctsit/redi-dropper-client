"""
Goal: Store helper functions not tied to a specific module

@authors:
    Andrei Sura             <sura.andrei@gmail.com>
    Ruchi Vivek Desai       <ruchivdesai@gmail.com>
    Sanath Pasumarthy       <sanath@ufl.edu>
"""

import os
from datetime import datetime, timedelta
import json
from flask import flash, request
from hashlib import sha512, sha256
import hmac
import base64

# @TODO: move to the configs
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff',
                          'zip', 'tar', 'tgz', 'bz2'])

FLASH_CATEGORY_ERROR = 'error'
FLASH_CATEGORY_INFO = 'info'


def _get_remote_addr():
    """ Return the utf-8 encoded request address """
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is not None:
        address = address.encode('utf-8')
    return address


def _get_user_agent():
    """ Return the utf-8 encoded request user agent """
    user_agent = request.headers.get('User-Agent')
    if user_agent is not None:
        user_agent = user_agent.encode('utf-8')
    return user_agent


def _create_salt():
    """ Get the first 16 bytes of the sha256(rand:user_ip:user_agent) """
    rand = base64.b64encode(os.urandom(24))

    base = '{0}:{1}:{2}'.format(rand, _get_remote_addr(), _get_user_agent())
    if str is bytes:
        base = unicode(base, 'utf-8', errors='replace')  # pragma: no cover
    hasher = sha256()
    hasher.update(base.encode('utf8'))
    all64 = hasher.hexdigest()
    return all64[0:16]


def _generate_sha512_hmac(pepper, salt, data):
    """ Generate the SHA512 HMAC -- for compatibility with Flask-Security
    h = HMAC(pepper, salt+data)

    Where
        pepper: the global application key
        salt:   the 128bit (16bytes) obtained from sha256(rand:ip:agent)
        data:   the data to be protected

from passlib.context import CryptContext
self.password_crypt_context = CryptContext(schemes='bcrypt')
    """
    payload = '{}:{}'.format(salt.encode('utf-8'), data.encode('utf-8'))
    return base64.b64encode(hmac.new(pepper, payload, sha512).digest())


def generate_auth(pepper, password):
    """
    Return the salt and hashed password to be stored in the database.
    Execute once when the user account is created.

    Note: requires a request context.
    """
    salt = _create_salt()
    hashed_pass = _generate_sha512_hmac(pepper, salt, password)
    return (salt, hashed_pass)


def is_valid_auth(pepper, salt, candidate_password, correct_hash):
    """
    Return ``True`` if the candidate_password hashes to the same
    value stored in the database as correct_hash.

    :param pepper: the global application security key
    :param salt: the user-specific salt
    :param candidate_password

    :rtype Boolean
    :return password validity status
    """
    assert pepper is not None
    assert salt is not None
    assert candidate_password is not None
    candidate_hash = _generate_sha512_hmac(pepper, salt, candidate_password)
    return correct_hash == candidate_hash


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


def pack(data):
    """
    Create a string represenation of data
    :param data -- dictionary
    """
    return json.dumps(data)


def pack_error(msg):
    """ Format an error message to be json-friendly """
    return pack({'status': 'error', 'message': msg})


def pack_info(msg):
    """ Format an info message to be json-friendly """
    return pack({'status': 'info', 'message': msg})


def pack_success_result(data):
    """ Format a success message to be json-friendly """
    return pack({'status': 'success', 'data': data})


def get_db_friendly_date_time():
    """
    :rtype: string
    :return current time in format: "2014-06-24 01:23:24"
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


def get_expiration_date(offset_days):
    """
    :param offset_days: how many days to shift versus today
    :rtype datetime
    :return the date computed with offset_days
    """
    return datetime.now() + timedelta(days=offset_days)
