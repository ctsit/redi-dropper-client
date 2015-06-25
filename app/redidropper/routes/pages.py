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
import datetime
import uuid
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from redidropper.models.log_entity import LogEntity
from redidropper.models.web_session_entity import WebSessionEntity
from wtforms import Form, TextField, PasswordField, validators

from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user
from flask_principal import \
    Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed

from redidropper.main import app
from redidropper import utils
from redidropper.models.user_entity import UserEntity

# set the login manager for the app
login_manager = LoginManager(app)

# Possible options: strong, basic, None
login_manager.session_protection = "strong"
login_manager.login_message = ""
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Return the user from the database"""
    return UserEntity.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """ Returns a message for the unauthorized users """
    # return redirect('/')
    return 'Please <a href="{}">login</a> first.'.format(url_for('index'))


# @app.errorhandler(403)
# def page_not_found(e):
#     """
#     Redirect to login page if probing a protected resources before login
#     """
#     show_permission_error = True
#     if show_permission_error:
#         # session['redirected_from'] = request.url
#         return redirect(url_for('index') + "?next={}".format(request.url))


class LoginForm(Form):
    """ Declare the validation rules for the login form """
    # email = TextField('Email', [validators.Length(min=4, max=25)])
    email = TextField('Email')
    password = PasswordField(
        'Password', [
            validators.Required(), validators.Length(
                min=6, max=25)])


@app.before_request
def check_session_id():
    """
    Generate a UUID and store it in the session
    as well as in the WebSession table.
    """
    # TODO: Create UserAgentEntity and populate
    user_agent_id = 1

    if 'uuid' not in session:
        session['uuid'] = str(uuid.uuid4())
        WebSessionEntity.create(session_id=session['uuid'],
                                user_id=current_user.get_id(),
                                ip=request.remote_addr,
                                date_time=datetime.datetime.now(),
                                user_agent_id=user_agent_id)
    else:
        # TODO: update the user_id on the first request after login is completed
        pass


@app.route('/', methods=['POST', 'GET'])
def index():
    """ Render the login page"""

    if app.config['LOGIN_USING_SHIB_AUTH']:
        return render_login_shib()
    return render_login_local()


def render_login_local():
    """ Render the login page with username/pass"""
    if current_user.is_authenticated():
        next_page = get_role_landing_page()
        return redirect(next_page)

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
            LogEntity.login(str(session['uuid']),
                            "No such email: {}".format(email))
            return redirect(url_for('index'))

        # if utils.is_valid_auth(app.config['SECRET_KEY'], auth.uathSalt,
        # password, auth.uathPassword):
        if '' == user.password_hash:
            app.logger.info('Log login event for: {}'.format(user))
            LogEntity.login(str(session['uuid']),
                            'Successful login via email/password')
            # Pass force=True to ignore is_active=false
            login_user(user, remember=False, force=False)

            # Tell Flask-Principal that the identity has changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.get_id()))
            next_page = get_role_landing_page()
            return redirect(next_page)
        else:
            app.logger.info('Incorrect pass for: {}'.format(user))
            LogEntity.login_error(str(session['uuid']),
                                  'Incorrect pass for: {}'.format(user))

    return render_template('index.html', form=form)


@app.route('/loginExternalAuth', methods=['POST', 'GET'])
def shibb_redirect():
    """
    Redirect to the local shibboleth instance where
    we can pass the return path.
    This route is reached when the user clicks the "Login" button.
    Note: This is equivalent to Apache's syntax:
        Redirect seeother /loginExternalAuth /Shibboleth.sso/Login?target=...

    @see #shibb_return()
    """
    next_page = "/Shibboleth.sso/Login?target={}"\
                .format(url_for('shibb_return'))
    return redirect(next_page)


@app.route('/loginExternalAuthReturn', methods=['POST', 'GET'])
def shibb_return():
    """
    Read the Shibboleth headers returned by the IdP after
    the user entered the usrname/password.
    If the `eduPersonPrincipalName` (aka Eppn) for the user matches the
    usrEmail of an active user then let the user in,
    otherwise let them see the login page.

    @see #shibb_redirect()
    """
    if current_user.is_authenticated():
        # already logged in...
        next_page = get_role_landing_page()
        return redirect(next_page)

    # fresh login
    email = request.headers['Mail']
    glid = request.headers['Glid']  # Gatorlink ID
    app.logger.debug("Checking if email: {} is registered for glid: {}"
                     .format(email, glid))
    user = UserEntity.query.filter_by(email=email).first()

    if not user:
        utils.flash_error("No such user: {}".format(email))
        # log_event("Shibboleth user not allowed for this resource")
        return redirect(url_for('index'))

    if not user.is_active():
        utils.flash_error("Inactive user: {}".format(email))
        # log_event("Inactive user tries to login")
        return redirect(url_for('index'))

    if user.is_expired():
        utils.flash_error("User account for {} expired on {}"
                          .format(email, user.access_expires_at))
        # log_event("Expired user tries to login")
        return redirect(url_for('index'))

    # Log it
    app.logger.info('Successful login via Shibboleth for: {}'.format(user))
    LogEntity.login(str(session['uuid']), 'Successful login via Shibboleth')

    login_user(user, remember=False, force=False)

    # Tell Flask-Principal that the identity has changed
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.get_id()))
    next_page = get_role_landing_page()
    return redirect(next_page)


def render_login_shib():
    """ Render the login page with button redirecting to
    Shibboleth /loginExternalAuth path
    """
    return render_template('login_shib.html', form=request.form)


def get_role_landing_page():
    """
    Get the landing page for a user with specific role
    :return None if the user has no roles
    """
    if not hasattr(current_user, 'roles'):
        return None

    # roles = current_user.get_roles()

    # if ROLE_ADMIN in roles:
    #     role_landing_page = url_for('admin')
    # elif ROLE_TECHNICIAN in roles:
    #     role_landing_page = url_for('start_upload')
    # elif ROLE_RESEARCHER_ONE in roles:
    #     role_landing_page = url_for('researcher_one')
    # elif ROLE_RESEARCHER_TWO in roles:
    #     role_landing_page = url_for('researcher_two')

    # app.logger.info("Found roles: {}".format(roles))
    # return request.args.get('next') or role_landing_page

    # Per Chris's request all users land on the same page
    return url_for('start_upload')


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
            # app.logger.debug("Provide role: {}".format(role))
            identity.provides.add(RoleNeed(role.name))


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
        md5 = hashlib.md5()
        md5.update(api_key)
        app.logger.debug("trying api_key: {}".format(md5.digest()))
        user = UserEntity.query.filter_by(api_key=api_key).first()
        return user

    # finally, return None if neither of the api_keys is valid
    return None


@app.route('/logout')
def logout():
    """ Destroy the user session and redirect to the home page

    Shib:
        https://shib.ncsu.edu/docs/logout.html
        https://wiki.shibboleth.net/confluence/display/CONCEPT/SLOIssues
    """
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    # Log the logout
    LogEntity.logout(str(session['uuid']))

    return redirect(request.args.get('next') or '/')
