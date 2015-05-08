# This file contains pytest 'fixtures'.
#
# Note: pytest expects this file to be named 'conftest.py'
#
# If a test function specifies the name of a fixture function as a parameter,
# then the fixture function is called and its result is passed to the test
# function.

import pytest

from redidropper.main import app as flask_app
from redidropper.main import db as sqlalchemy_db
from redidropper.startup import initializer


#class TestProxy(object):
#    ''' Helper class for setting the testing environment '''
#    def __init__(self, app):
#        self.app = app
#
#    def __call__(self, environ, start_response):
#        environ = {
#                'REMOTE_ADDR': os.environ.get('REMOTE_ADDR', '127.0.0.1'),
#                'HTTP_USER_AGENT': os.environ.get('HTTP_USER_AGENT', 'Chrome'),
#                }
#        return self.app(environ, start_response)


@pytest.fixture(scope='module')
def app():
    """
    Init the application object.
    Note: We pass "extra_settings" to the function
        {@link redidropper.startup.initializer.do_init()}

    rtype Flask
    :return the application object
    """
    # Initialize the Flask-App with test-specific settings
    test_settings = dict(
        # show exceptions
        TESTING=True,

        # Enable url_for() without request context
        SERVER_NAME='localhost',

        # Enable @register_required
        LOGIN_DISABLED=False,

        # Disable Flask-Mail send
        MAIL_SUPPRESS_SEND=True,

        # use the in-memory database
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        # SQLALCHEMY_DATABASE_URI='sqlite:///db.test',

        # Disable CSRF form validation
        WTF_CSRF_ENABLED=False,

    )

    initializer.do_init(flask_app, sqlalchemy_db, test_settings)
    # Add context because we run outside of the webserver context
    flask_app.app_context().push()

    return flask_app

@pytest.fixture(scope='module')
def db():
    """
    :return the initialized db object
    """
    return sqlalchemy_db
