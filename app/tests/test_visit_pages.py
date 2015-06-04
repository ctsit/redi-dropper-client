"""
Goal: Simulate browsing of the pages in the url_map

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

from __future__ import print_function

from flask import url_for
from .base_test_with_data import BaseTestCaseWithData
from redidropper.main import app

protected_pages = [
    '/admin',
    '/dashboard',
    '/researcher_one',
    '/researcher_two',
    '/start_upload',
    '/download_file',
    '/logs',
    ]


class TestVisitPages(BaseTestCaseWithData):

    """ ha """

    def test_visit_pages(self):
        """ Verify the pages without params such as home/ about/ contact."""
        print("")

        for rule in app.url_map.iter_rules():
            if 'static' == rule.endpoint:
                continue

            url = url_for(rule.endpoint)

            # Calculate number of default-less parameters
            params = len(rule.arguments) if rule.arguments else 0
            params_with_default = len(rule.defaults) if rule.defaults else 0
            params_without_default = params - params_with_default

            # Skip routes with default-less parameters
            if params_without_default > 0:
                print("Skip parametrized page: {}".format(url))
                continue

            # Skip routes without a GET method
            if 'GET' not in rule.methods:
                print("Skip non-get page: {}".format(url))
                continue

            # Skip routes for protcted_pages
            if url in protected_pages:
                print("Skip special page: {}".format(url))
                continue

            # Simulate visiting the page
            print("Visiting page: {}".format(url))
            result = self.client.get(url, follow_redirects=True)
            print(result)

    def test_login(self):
        """ TODO: add user to database first """
        login_url = url_for('index')
        login_data = {'email': 'admin@example.com', 'password': 'password'}
        response = self.client.post(login_url, login_data)
        print("Try to login response: {}".format(response))
        # self.assert_redirects(response, url_for('technician'))
