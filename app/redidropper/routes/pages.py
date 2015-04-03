"""
Goal: Define the routes for general pages

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""
from flask import request

from flask import url_for
from flask import redirect
from flask import render_template

from flask.ext.login import LoginManager, login_user, logout_user
from flask.ext.login import login_required, current_user
from flask.ext.principal import Principal, Permission, RoleNeed

from wtforms import Form, TextField, PasswordField
from wtforms import validators

from redidropper.main import app
from redidropper import utils
from redidropper.models import dao

# load the Principal extension
principals = Principal(app)

# set the login manager for the app
# then define the `load_user` method

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(userid):
    """Return the user from the database"""
    return dao.find_user(usrID=userid)


class LoginForm(Form):
    username    = TextField('Username', [validators.Length(min=4, max=25)])
    password    = PasswordField('Password', [validators.Required()])


@app.route('/', methods=['POST','GET'])
def index():
    """ Render the home page """
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data.strip() if form.username.data else ""
        password = form.password.data.strip()

        auth = dao.find_auth_by_username(username)
        if auth:
            app.logger.info("Found auth object: {}".format(auth.uathID))
        else:
            utils.flash_error("No such account")
            return redirect('/')

        # @TODO: hash before comparing
        if password == auth.uathPassword:
            project_id = 1
            role = dao.find_role_by_username_and_projectid(username, project_id)
            app.logger.info('welcome {}'.format(username))
            app.logger.info("Found role: {}".format(role))
            utils.flash_info('Welcome {}'.format(auth))
            return redirect(url_for('technician'))
        else:
            app.logger.info('Incorrect pass')
            utils.flash_error("Incorrect password.")

    return render_template('pages/index.html', form=form)


@app.route('/logout')
def logout():
    """ Destroy the user session and redirect to the home page """
    #session.pop('user')
    return redirect('/')


@app.route('/about')
def about():
    """ Render the about page """
    return render_template('pages/about.html')


@app.route('/contact')
def contact():
    return render_template('pages/contact.html')
