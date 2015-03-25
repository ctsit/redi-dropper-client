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


