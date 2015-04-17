"""
Implement the default-config and test-config clases
"""

import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig(object):
    """ Default configuration data """

    DEBUG = False
    TESTING = False

    ADMINS = frozenset(['admin@example.com'])
    SECRET_KEY = ''

    # THREADS_PER_PAGE = 8

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = ""

    DB_USER = ''
    DB_PASS = ''
    DB_HOST = ''
    DB_NAME = ''
    SQLALCHEMY_DATABASE_URI = "mysql..."


class DebugConfig(DefaultConfig):
    """ Extra flag for debugging """
    DEBUG = True


class TestConfig(DefaultConfig):
    """ Configuration for running tests """
    TESTING = True
    CSRF_ENABLED = False

    DATABASE = 'tests.db'
    DATABASE_PATH = os.path.join(_basedir, DATABASE)

    run_fast = True
    if run_fast:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        # If we want to inspect the results we can use a file instead of memory
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
