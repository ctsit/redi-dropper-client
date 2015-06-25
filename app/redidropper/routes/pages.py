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
from redidropper.models.log_type_entity import LogTypeEntity
from redidropper.models.web_session_entity import WebSessionEntity
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


@app.errorhandler(403)
def page_not_found(e):
    """
    Redirect to login page if probing a protected resources before login
    """
    show_permission_error = True
    if show_permission_error:
        # session['redirected_from'] = request.url
        return redirect(url_for('index') + "?next={}".format(request.url))


class LoginForm(Form):

    """ Declare the validation rules for the login form """
    # email = TextField('Email', [validators.Length(min=4, max=25)])
    email = TextField('Email')
    # username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField(
        'Password', [
            validators.Required(), validators.Length(
                min=6, max=25)])


@app.before_request
def check_session_id():
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
        WebSessionEntity.create(session_id=session['uuid'],
                                user_id=0,
                                ip=request.remote_addr,
                                date_time=datetime.datetime.now(),
                                 # TODO: Create UserAgentEntity and populate
                                user_agent_id=1)


@app.route('/', methods=['POST', 'GET'])
def index():
    """ Render the login page"""

    if app.config['LOGIN_USING_SHIB_AUTH']:
        return render_login_shib()
    return render_login_local()


def render_login_local():
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
            LogEntity.login(session['uuid'], "No such email: {}".format(email),
                            successful=False)
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
            LogEntity.login(session['uuid'],
                            'Log login event for: {}'.format(user))
            next_page = get_role_landing_page()
            # utils.flash_info("next page: ".format(request.args.get('next')))
            # return redirect(request.args.get('next') or next_page)
            return redirect(next_page)
        else:
            app.logger.info('Incorrect pass')
            LogEntity.login(session['uuid'],
                            'Incorrect pass for: {}'.format(user),
                            successful=False)
            utils.flash_error("Incorrect password.")

    if current_user.is_authenticated():
        next_page = get_role_landing_page()
        # utils.flash_info("next page: ".format(request.args.get('next')))
        # return redirect(request.args.get('next') or next_page)
        return redirect(next_page)

    return render_template('index.html', form=form)


@app.route('/loginExternalAuthReturn/', methods=['POST', 'GET'])
def shib_return():
    """ Helper for reading the Shibboleth headers """
    # import pprint; pprint.pprint(request.headers)
    interesting_fields = ['Mail', 'Eppn', 'Glid']
    data = [i for i in request.headers if i[0] in interesting_fields]
    LogEntity.login(session['uuid'], 'Successful login via Shibboleth: {}',
                    utils.jsonify_success(data))
    return utils.jsonify_success({'headers': data})


def render_login_shib():
    """
    Login page for using Shibboleth /loginExternalAuth path
    """
    return render_template('login_shib.html', form=request.form)


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
    LogEntity.logout(session['uuid'], 'User logged out.')

    return redirect(request.args.get('next') or '/')


# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('js', path)
