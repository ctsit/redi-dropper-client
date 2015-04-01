"""
Define the routes for the users
"""
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template

from flask_user import login_required, roles_required

from redidropper.main import app

@app.route('/users/admin')
def admin():
    """ Render the technician's home page """
    return render_template('users/admin.html')


@app.route('/users/technician')
def technician():
    """ Render the technician's home page """
    return render_template('users/technician.html')

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

@app.route('/users/manage_event')
@app.route('/users/manage_event/<event_id>')
def upload(event_id=None):
    """ Render the upload screen """
    return render_template('users/manage_event.html',event_id=event_id)


