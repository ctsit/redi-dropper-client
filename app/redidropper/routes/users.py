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
    return render_template('logs.html', user_links=get_user_links())


def get_highest_role():
    """ If a user has more than one role pick the `highest` role """
    roles = current_user.get_roles()

    if ROLE_ADMIN in roles:
        return ROLE_ADMIN
    if ROLE_TECHNICIAN in roles:
        return ROLE_TECHNICIAN
    if ROLE_RESEARCHER_ONE in roles:
        return ROLE_RESEARCHER_ONE
    if ROLE_RESEARCHER_TWO in roles:
        return ROLE_RESEARCHER_TWO
    return None


def get_user_links():
    pages = {
        'admin': ('admin', 'Manage Users'),
        'logs': ('logs', 'View Logs'),
        'dashboard': ('dashboard', 'Dashboard'),
        'res_one': ('researcher_one', 'Researcher 1'),
        'res_two': ('researcher_two', 'Researcher 2'),
        'start_upload': ('start_upload', 'Start Upload'),
        'logout': ('logout', 'Logout'),
    }
    role = get_highest_role()
    print "highest role: {}".format(role)

    if ROLE_ADMIN == role:
        links = [pages['admin'], pages['start_upload'], pages['dashboard'],
                 pages['logs']]
    elif ROLE_TECHNICIAN == role:
        links = [pages['start_upload'], pages['dashboard']]
    elif ROLE_RESEARCHER_ONE == role:
        links = [pages['res_one']]
    elif ROLE_RESEARCHER_TWO == role:
        links = [pages['res_two']]

    links.append(pages['logout'])
    return links


@app.route('/dashboard')
@perm_admin_or_technician.require()
def dashboard():
    """ Render the technician's home page """
    return render_template('dashboard.html', user_links=get_user_links())


@app.route('/researcher_one')
@perm_researcher_one.require()
def researcher_one():
    """ Render the researcher's home page """
    return render_template('researcher_one.html',
                           user_links=get_user_links())


@app.route('/researcher_two')
@perm_researcher_two.require()
def researcher_two():
    """ Render the researcher's home page """
    return render_template('researcher_two.html',
                           user_links=get_user_links())


@app.route('/start_upload')
@perm_admin_or_technician.require()
def start_upload():
    """ Render the Start Upload page """
    # @roles_accepted(ROLE_ADMIN, ROLE_TECHNICIAN)
    return render_template('start_upload.html',
                           user_links=get_user_links())


@app.route("/download_file")
@app.route("/download_file/<file_id>")
@login_required
def download_file(file_id):
    """ Download a file using the database id """
    file_path = file_manager.get_file_path_from_id(file_id)
    return send_file(file_path, as_attachment=True)
