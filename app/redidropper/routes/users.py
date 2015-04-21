"""
Goal: Define the routes for the users

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

# from flask import request
from flask import render_template
from flask import send_file

from flask_login import login_required, current_user
from flask_principal import Principal, Permission, RoleNeed

from redidropper.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN
from redidropper.main import app
from redidropper.routes.managers import file_manager

# from pages import ProjectRolePermission
# load the Principal extension
principals = Principal(app)

# define a permission
perm_admin = Permission(RoleNeed(ROLE_ADMIN))
perm_admin_or_technician = Permission(RoleNeed(ROLE_ADMIN),
                                      RoleNeed(ROLE_TECHNICIAN))


@app.route('/admin')
@perm_admin.require()
def admin():
    """ Render the technician's home page
    @perm_admin_or_technician.require()
    from flask import abort
    abort(403)
    """
    return render_template('admin.html')


@app.route('/logs')
@login_required
def logs():
    """ Render the logs for the user """
    return render_template('logs.html')


def get_user_links():
    current_role = 'admin'
    all_pages = [
        ('index', 'Home'), \
        ('technician', 'Dashboard'), \
        ('start_upload', 'Start Upload'),
        ('logout', 'Logout'), \
    ]

    pages = {
        'admin': all_pages,
        'technician': all_pages,
    }
    return pages[current_role]


@app.route('/users/technician')
@login_required
def technician():
    """ Render the technician's home page """
    user_links = get_user_links()
    return render_template('users/technician.html', current_user=current_user, \
        user_links=user_links)

@app.route('/users/start_upload')
@login_required
def start_upload():
    """ Render the Start Upload page """
    user_links = get_user_links()
    return render_template('users/start_upload.html',user_links=user_links)


@app.route('/users/project')
@app.route('/users/project/<project_id>/subject/<subject_id>')
@login_required
def project_subject_files(project_id=None, subject_id=None):
    """ Render the project subject files page """
    return render_template('users/project_subject_files.html',
                           subject_id=subject_id, project_id=project_id)


@app.route('/users/researcher_one')
@login_required
def researcher_one():
    """ Render the researcher's home page """
    return render_template('users/researcher_one.html')


@app.route('/users/researcher_two')
@login_required
def researcher_two():
    """ Render the researcher's home page """
    return render_template('users/researcher_two.html')


@app.route('/users/manage_event')
@app.route('/users/manage_event/<event_id>')
@login_required
def manage_event(event_id=None):
    """ Render the upload screen """
    return render_template('users/manage_event.html', event_id=event_id)


@app.route("/users/download_file/<file_id>")
@login_required
def download_file(file_id):
    """ Download a file using the database id """
    file_path = file_manager.get_file_path_from_id(file_id)
    return send_file(file_path, as_attachment=True)
