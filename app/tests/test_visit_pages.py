# Simulate browsing of the pages which do not require parameters
#
# Authors:
#   Andrei Sura <sura.andrei@gmail.com>

from __future__ import print_function
from flask import url_for

def test_visit_pages(app):
    """
    Verify the unsecured pages such as home/ about/ contact.
    """
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
        client = app.test_client()

        # Simulate visiting the page
        url = url_for(rule.endpoint)
        print("Visiting page: {}".format(url))
        result = client.get(url, follow_redirects=True)
        print(result)

    return
