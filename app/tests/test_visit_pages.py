# Simulate browsing of the pages which do not require parameters
#
# Authors:
#   Andrei Sura <sura.andrei@gmail.com>

from __future__ import print_function

from datetime import datetime
from flask import url_for
from .base_test import BaseTestCase
from redidropper.main import app
from redidropper import utils
from redidropper.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN
from redidropper.models.user_entity import UserEntity
from redidropper.models.role_entity import RoleEntity



class TestVisitPages(BaseTestCase):

    """ ha """

    def test_visit_pages(self):
        """ Verify the pages without params such as home/ about/ contact."""
        print("")

        for rule in app.url_map.iter_rules():
            # Calculate number of default-less parameters
            params = len(rule.arguments) if rule.arguments else 0
            params_with_default = len(rule.defaults) if rule.defaults else 0
            params_without_default = params - params_with_default

            # Skip routes with default-less parameters
            if params_without_default > 0:
                continue

            # Skip routes without a GET method
            if 'GET' not in rule.methods:
                continue

            # Retrieve a browser client simulator from the Flask app
            # client = app.test_client()
            client = self.client

            # Simulate visiting the page
            url = url_for(rule.endpoint)
            print("Visiting page: {}".format(url))
            result = client.get(url, follow_redirects=True)
            print(result)

    def create_admin(self):
        added_date = datetime.today()
        access_end_date = utils.get_expiration_date(180)
        user = UserEntity.create(email="admin@example.com",
                                 first="",
                                 last="",
                                 minitial="",
                                 added_at=added_date,
                                 modified_at=added_date,
                                 access_expires_at=access_end_date)
        role_admin =  RoleEntity.create(name=ROLE_ADMIN, description='role')
        user.roles.append(role_admin)


    def test_login(self):
        """ TODO: add user to database first """
        self.create_admin()
        login_url = url_for('index')
        login_data = {'email': 'admin@example.com', 'password': 'password'}
        response = self.client.post(login_url, login_data)
        print(response)
        self.assert_redirects(response, url_for('technician'))
