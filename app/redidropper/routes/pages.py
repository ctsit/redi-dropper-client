"""
Goal: Define the routes for general pages

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from wtforms import Form, TextField, PasswordField, validators

#import flask.ext.login as flask_login
from flask_login import LoginManager, login_user, logout_user
#, Permission, RoleNeed
from flask_principal import Principal, \
    Identity, AnonymousIdentity, identity_changed


from redidropper.main import app
from redidropper import utils
from redidropper.models import dao

# load the Principal extension
Principal(app)

# set the login manager for the app
LOGIN_MANAGER = LoginManager(app)

@LOGIN_MANAGER.user_loader
def load_user(userid):
    """Return the user from the database"""
    return dao.find_user_by_id(userid)

"""
Declare the validation rules for the login form
"""
class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', \
            [validators.Required(), validators.Length(min=6, max=25)])


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

        # @TODO: hash before comparing
        if password == auth.uathPassword:
            # Keep the user info in the session using Flask-Login
            user = auth.user
            # Pass remember=True to remember
            # Pass force=True to ignore is_active=false
            login_user(user, remember=False, force=False)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.get_id()))

            project_id = 1
            role = dao.find_role_by_username_and_projectid(username, project_id)
            app.logger.info('Role {}'.format(role))
            utils.flash_info('Role {}'.format(role))
            return redirect(request.args.get('next') or url_for('technician'))
        else:
            app.logger.info('Incorrect pass')
            utils.flash_error("Incorrect password.")

    return render_template('pages/index.html', form=form)


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


@app.route('/about')
def about():
    """ Render the about page """
    return render_template('pages/about.html')


@app.route('/contact')
def contact():
    """ Render the contact page """
    return render_template('pages/contact.html')
