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

from redidropper.models.role_entity import \
    ROLE_ADMIN, ROLE_TECHNICIAN, ROLE_RESEARCHER_ONE, ROLE_RESEARCHER_TWO
from redidropper.main import app
from redidropper.routes.managers import file_manager

# @TODO: read https://pythonhosted.org/Flask-Security/api.html
# from flask_security import roles_accepted
# from flask_security import roles_required, auth_token_required

# from pages import ProjectRolePermission
# load the Principal extension
principals = Principal(app)

# define a permission
perm_admin = Permission(RoleNeed(ROLE_ADMIN))
perm_technician = Permission(RoleNeed(ROLE_TECHNICIAN))
perm_researcher_one = Permission(RoleNeed(ROLE_RESEARCHER_ONE))
perm_researcher_two = Permission(RoleNeed(ROLE_RESEARCHER_TWO))
perm_admin_or_technician = Permission(RoleNeed(ROLE_ADMIN),
                                      RoleNeed(ROLE_TECHNICIAN))


@app.route('/admin')
@perm_admin.require()
def admin():
    """ Render the technician's home page
    from flask import abort
    abort(403)
    """
    return render_template('admin.html', user_links=get_user_links())


@app.route('/logs')
@perm_admin_or_technician.require()
def logs():
    """ Render the logs for the user """
    return render_template('logs.html')


def get_user_links():
    current_role = 'admin'
    all_pages = [
        # ('index', 'Home'),
        ('admin', 'Admin'),
        ('logs', 'Logs'),
        ('technician', 'Technician'),
        ('researcher_one', 'Researcher 1'),
        ('researcher_two', 'Researcher 2'),
        ('start_upload', 'Start Upload'),
        ('logout', 'Logout'),
    ]

    pages = {
        'admin': all_pages,
        'technician': all_pages,
    }
    return pages[current_role]


@app.route('/technician')
@perm_admin_or_technician.require()
def technician():
    """ Render the technician's home page """
    user_links = get_user_links()
    return render_template('users/technician.html', current_user=current_user,
                           user_links=user_links)


@app.route('/start_upload')
@perm_admin_or_technician.require()
def start_upload():
    """ Render the Start Upload page """
    # @roles_accepted(ROLE_ADMIN, ROLE_TECHNICIAN)
    user_links = get_user_links()
    return render_template('users/start_upload.html', user_links=user_links)


# @app.route('/subject')
# @app.route('/subject/<subject_id>')
# @login_required
# def list_subject_files(subject_id=None):
#     """ Render the subject files page """
#     return render_template('users/project_subject_files.html',
#                            subject_id=subject_id)


@app.route('/researcher_one')
@perm_researcher_one.require()
def researcher_one():
    """ Render the researcher's home page """
    return render_template('users/researcher_one.html')


@app.route('/researcher_two')
@perm_researcher_two.require()
def researcher_two():
    """ Render the researcher's home page """
    return render_template('users/researcher_two.html')


# @app.route('/users/manage_event')
# @app.route('/users/manage_event/<event_id>')
# @login_required
# def manage_event(event_id=None):
#     """ Render the upload screen """
#     return render_template('users/manage_event.html', event_id=event_id)


@app.route("/users/download_file/<file_id>")
@login_required
def download_file(file_id):
    """ Download a file using the database id """
    file_path = file_manager.get_file_path_from_id(file_id)
    return send_file(file_path, as_attachment=True)
