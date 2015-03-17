from flask import Flask
from flask import session
from flask import redirect

from flask_sso import SSO
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
sso = SSO(app=app)


#: Default attribute map
SSO_ATTRIBUTE_MAP = {
    'ADFS_AUTHLEVEL': (False, 'authlevel'),
    'ADFS_GROUP': (True, 'group'),
    'ADFS_LOGIN': (True, 'nickname'),
    'ADFS_ROLE': (False, 'role'),
    'ADFS_EMAIL': (True, 'email'),
    'ADFS_IDENTITYCLASS': (False, 'external'),
    'HTTP_SHIB_AUTHENTICATION_METHOD': (False, 'authmethod'),
}

# @TODO: move to the config.py
app.config.setdefault('SSO_ATTRIBUTE_MAP', SSO_ATTRIBUTE_MAP)
app.config.setdefault('SSO_LOGIN_URL', "https://login.ufl.edu/idp/Authn/UserPassword")

# Attach the toolbar when debug = True
toolbar = DebugToolbarExtension(app)

# import route handlers
import redidropper.views


@sso.login_handler
def login(user_info):
    """Store information in session."""
    #https://www.snip2code.com/Snippet/210654/A-Flask-application-configured-to-accept
    session["user"] = user_info
    return redirect('/')

