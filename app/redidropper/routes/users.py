"""
Goal: Define the routes for the users

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

#from flask_user import login_required, roles_required

from redidropper.main import app
from redidropper.models import dao

# load the Principal extension
principals = Principal(app)

# define a permission
admin_permission = Permission(RoleNeed('admin'))


@app.route('/users/admin')
@admin_permission.require()
def admin():
    """ Render the technician's home page """
    return render_template('users/admin.html')


@app.route('/users/technician')
def technician():
    """ Render the technician's home page """
    return render_template('users/technician.html', is_loggedin=True)

@app.route('/users/project')
@app.route('/users/project/<project_id>/subject/<subject_id>')
def project_subject_files(project_id=None,subject_id=None):
    """ Render the project subject files page """
    return render_template('users/project_subject_files.html',subject_id=subject_id,project_id=project_id)

@app.route('/users/researcher_one')
def researcher_one():
    """ Render the researcher's home page """
    return render_template('users/researcher_one.html')


@app.route('/users/researcher_two')
def researcher_two():
    """ Render the researcher's home page """
    return render_template('users/researcher_two.html')

@app.route('/users/upload')
@app.route('/users/upload/<subject_id>')
def upload(subject_id=None):
    """ Render the upload screen """

    return render_template('users/upload.html',subject_id=subject_id)


