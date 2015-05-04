"""
Goal: Define the routes for the users

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

# from flask import request
from flask import render_template

from flask_login import current_user
from flask_principal import Principal, Permission, RoleNeed

from redidropper.models.role_entity import \
    ROLE_ADMIN, ROLE_TECHNICIAN, ROLE_RESEARCHER_ONE, ROLE_RESEARCHER_TWO
from redidropper.main import app

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
    """ If a user has more than one role pick the `highest` role

    :rtype string
    :return the role name for the current_user or None
    """

    try:
        roles = current_user.get_roles()
    except Exception as exc:
        app.logger.debug("get_highest_role() problem: {}".format(exc))
        return None

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
    """
    :rtype list
    :return the navigation menu options depending on the role or None if
        the current_user doe not have a role
    """
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
    if role is None:
        return []

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


@app.route('/api')
@app.route('/api/')
def api():
    """ Display the list of valid paths under /api/ """
    # @TODO: protect with @perm_admin.require() when unit tests are fixed
    return render_template('api.html', user_links=get_user_links())
