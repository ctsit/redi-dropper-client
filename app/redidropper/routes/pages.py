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
#from collections import namedtuple
from functools import partial

from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from wtforms import Form, TextField, PasswordField, validators

from flask_login import LoginManager, AnonymousUserMixin, \
        login_user, logout_user, current_user
from flask_principal import \
    Identity, AnonymousIdentity, identity_changed, identity_loaded, \
    Permission, Need #, UserNeed, RoleNeed

from redidropper.main import app
from redidropper import utils
from redidropper.models import dao
#from redidropper.models.all import UserAuthEntity

#ProjectRoleNeed = namedtuple('project_role', ['role', 'value'])
PROJECT_ROLE_NEED = partial(Need, 'role')

#AdminProjectRoleNeed = partial(ProjectRoleNeed, 'admin')
#TechnicianProjectRoleNeed = partial(ProjectRoleNeed, 'technician')
#BlogPostNeed = namedtuple('blog_post', ['method', 'value'])
#EditiBlogPostNeed = partial(BlogPostNeed, 'edit')

class ProjectRolePermission(Permission):
    """ Custom permission object """

    def __init__(self, pur_id):
        """ Create a permission object using the ProjectUserRole.purID column"""
        need = PROJECT_ROLE_NEED(unicode(pur_id))
        super(ProjectRolePermission, self).__init__(need)


# load the Principal extension
#principals = Principal(app)

# set the login manager for the app
login_manager = LoginManager(app)

# Possible options: strong, basic, None
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(userid):
    """Return the user from the database"""
    return dao.find_user_by_id(userid)


@login_manager.unauthorized_handler
def unauthorized():
    """ Returns a message for the unauthorized users """
    # return redirect('/')
    return 'Please <a href="{}">login</a> first.'.format(url_for('index'))


class LoginForm(Form):
    """ Declare the validation rules for the login form """

    email_id = TextField('email Address')
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField(
        'Password', [
            validators.Required(), validators.Length(
                min=6, max=25)])


@app.route('/', methods=['POST', 'GET'])
def index():
    """ Render the home page """
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data.strip() if form.username.data else ""
        password = form.password.data.strip()

        auth = dao.find_auth_by_username(username)

        if auth:
            app.logger.debug("Found auth object: {}".format(auth))
        else:
            utils.flash_error("No such account")
            return redirect('/')

        #salt = utils._create_salt(); print "salt: " + salt

        # @TODO: hash before comparing
        if utils.is_valid_auth(app.config['SECRET_KEY'], auth.uathSalt, \
                password, auth.uathPassword):
            # Keep the user info in the session using Flask-Login
            user = auth.user
            # Pass remember=True to remember
            # Pass force=True to ignore is_active=false
            login_user(user, remember=False, force=False)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.get_id()))

            project_id = 1
            role = dao.find_role_by_username_and_projectid(
                username,
                project_id)
            app.logger.info('Role {}'.format(role))
            utils.flash_info('Role {}'.format(role))
            return redirect(request.args.get('next') or url_for('technician'))
        else:
            app.logger.info('Incorrect pass')
            utils.flash_error("Incorrect password.")

    return render_template('index.html', form=form)


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """ Describe what `needs` does this identity provide
    @TODO: add unit tests
        http://stackoverflow.com/questions/16712321/unit-testing-a-flask-principal-application
    """
    #app.logger.debug("identity_loaded signal sender: {}".format(sender))

    if type(current_user) == 'AnonymousUserMixin':
        return

    identity.user = current_user

    # Add the UserNeed to the identity
    #try:
    #    identity.provides.add(UserNeed(current_user.get_id()))
    #except AttributeError as ae:
    #    app.logger.error("Error for signal identity_loaded: {}".format(ae))

    try:
        for proj_role in current_user.project_roles:
            identity.provides.add(PROJECT_ROLE_NEED(proj_role.get_id()))
    except AttributeError as error:
        app.logger.error("Error for signal identity_loaded: {}".format(error))


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
        #auth = UserAuthEntity.query.filter_by(uathApiKey=api_key).first()
        auth = dao.find_auth_by_api_key(api_key)

        if auth and auth.user:
            return auth.user

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

