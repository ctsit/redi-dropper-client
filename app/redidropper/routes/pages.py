"""
Goal: Define the routes for general pages

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>


@see https://flask-login.readthedocs.org/en/latest/
@see https://pythonhosted.org/Flask-Principal/
"""

import hashlib
import base64
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from wtforms import Form, TextField, PasswordField, validators

from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user
from flask_principal import \
    Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed

from redidropper.main import app
from redidropper import utils
from redidropper.models.user_entity import UserEntity
from redidropper.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN, \
    ROLE_RESEARCHER_ONE, ROLE_RESEARCHER_TWO

# set the login manager for the app
login_manager = LoginManager(app)

# class AnonymousUser(AnonymousUserMixin):
#   """ fix AttributeError: 'AnonymousUserMixin' object has no attribute 'id'"""
#
#     def __init__(self):
#         """ ha """
#         self.id = None
#         self.roles = ()
# login_manager.anonymous_user = AnonymousUser

# Possible options: strong, basic, None
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    """Return the user from the database"""
    return UserEntity.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """ Returns a message for the unauthorized users """
    # return redirect('/')
    return 'Please <a href="{}">login</a> first.'.format(url_for('index'))


class LoginForm(Form):

    """ Declare the validation rules for the login form """
    # email = TextField('Email', [validators.Length(min=4, max=25)])
    email = TextField('Email')
    # username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField(
        'Password', [
            validators.Required(), validators.Length(
                min=6, max=25)])


@app.route('/', methods=['POST', 'GET'])
def index():
    """ Render the home page """
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data.strip(
            ) if form.email.data else "admin@example.com"
        password = form.password.data.strip() if form.password.data else ""
        app.logger.debug("{} password: {}".format(email, password))

        app.logger.debug("Checking email: {}".format(email))
        user = UserEntity.query.filter_by(email=email).first()

        if user:
            app.logger.debug("Found user object: {}".format(user))
        else:
            utils.flash_error("No such email: {}".format(email))
            return redirect(request.args.get('next') or url_for('index'))

        # if utils.is_valid_auth(app.config['SECRET_KEY'], auth.uathSalt,
        # password, auth.uathPassword):
        if '' == user.password_hash:
            # Keep the user info in the session using Flask-Login
            # Pass remember=True to remember
            # Pass force=True to ignore is_active=false
            login_user(user, remember=False, force=False)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.get_id()))

            app.logger.info('Log login event for: {}'.format(user))
            next_page = get_role_landing_page()
            return redirect(next_page)
        else:
            app.logger.info('Incorrect pass')
            utils.flash_error("Incorrect password.")

    if current_user.is_authenticated():
        next_page = get_role_landing_page()
        return redirect(next_page)

    return render_template('index.html', form=form)


def get_role_landing_page():
    """
    Get the landing page for a user with specific role
    :return None if the
    """
    if not hasattr(current_user, 'roles'):
        return None

    roles = current_user.get_roles()

    if ROLE_ADMIN in roles:
        role_landing_page = url_for('admin')
    elif ROLE_TECHNICIAN in roles:
        role_landing_page = url_for('start_upload')
    elif ROLE_RESEARCHER_ONE in roles:
        role_landing_page = url_for('researcher_one')
    elif ROLE_RESEARCHER_TWO in roles:
        role_landing_page = url_for('researcher_two')

    return request.args.get('next') or role_landing_page


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """ Describe what `needs` does this identity provide
    @TODO: add unit tests
        http://stackoverflow.com/questions/16712321/unit-testing-a-flask-principal-application
    """
    # app.logger.debug("identity_loaded signal sender: {}".format(sender))

    if type(current_user) == 'AnonymousUserMixin':
        return

    identity.user = current_user

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            # app.logger.debug("Found role: {}".format(role))
            identity.provides.add(RoleNeed(role.name))

    # try:
    #     identity.provides.add(UserNeed(current_user.get_id()))
    # except AttributeError as ae:
    #     app.logger.error("Error for signal identity_loaded: {}".format(ae))


@login_manager.request_loader
def load_user_from_request(req):
    """ To support login from both a url argument and from Basic Auth
     using the Authorization header

    @TODO: use for api requests?
        Need to add column `UserAuth.uathApiKey`
    """

    # first, try to login using the api_key url arg
    api_key = req.args.get('api_key')

    if not api_key:
        # next, try to login using Basic Auth
        api_key = req.headers.get('Authorization')
        if api_key:
            api_key = api_key.replace('Basic ', '', 1)
            try:
                api_key = base64.b64decode(api_key)
            except TypeError:
                pass

    if api_key:
        m = hashlib.md5()
        m.update(api_key)
        app.logger.debug("trying api_key: {}".format(m.digest()))
        user = UserEntity.query.filter_by(api_key=api_key).first()
        return user

    # finally, return None if neither of the api_keys is valid
    return None


@app.route('/logout')
def logout():
    """ Destroy the user session and redirect to the home page """
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(request.args.get('next') or '/')


# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('js', path)
