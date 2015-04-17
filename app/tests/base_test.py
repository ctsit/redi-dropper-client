"""
Goal: set the environment for tests
"""
from flask.ext.testing import TestCase
from redidropper.main import app, db
#from . import app, db


class BaseTestCase(TestCase):
    """ Base class for all tests"""

    def create_app(self):
        """ override the default config with the test config """ 
        app.config.from_object('config.TestConfig')
        return app


    def setUp(self):
        """ create all tables """
        db.create_all()


    def tearDown(self):
        """ remove all tables """
        db.session.remove()
        db.drop_all()
