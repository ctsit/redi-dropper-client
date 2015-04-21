"""
Goal: Implement the DAO

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

from sqlalchemy.orm.exc import NoResultFound
from redidropper.main import app, db

from redidropper.models.user_entity import UserEntity
from redidropper.models.user_auth_entity import UserAuthEntity
from redidropper.models.role_entity import RoleEntity



def find_user_by_id(user_id):
    """ Fetch the user object using the primary key

    :rtype: UserEntity
    """

    sess = app.db_session
    try:
        user = sess.query(UserEntity).filter_by(usrID=user_id).one()
        return user
    except NoResultFound:
        print "Unable to find row in find_user_by_id()"

    return None


def find_user_by_email(email):
    """ Fetch the user object using the email unique key

    :rtype: UserEntity
    """
    sess = app.db_session
    try:
        user = sess.query(UserEntity).filter_by(usrEmail=email).one()
        return user
    except NoResultFound:
        print "Unable to find row in find_user_by_email()"

    return None


def find_auth_by_username(username):
    """ Fetch the auth object for the specified username

    :rtype UserAuthEntity
    """
    sess = app.db_session
    try:
        auth = sess.query(UserAuthEntity).filter_by(
            uathUsername=username).one()
        return auth
    except NoResultFound:
        print "Unable to find row in find_auth_by_username()"

    return None


def find_auth_by_api_key(api_key):
    """ Fetch the auth object for the specified username

    :rtype UserAuthEntity
    """
    sess = app.db_session
    username = 'admin'
    # auth = sess.query(UserAuthEntity).filter_by(uathApiKey=api_key).one()
    auth = sess.query(UserAuthEntity).filter_by(
        uathUsername=username).one()
    return auth


def find_role_by_role_name(role_name):
    """ Fetch the role object for the specified role_name

    :rtype RoleEntity
    """
    sess = app.db_session
    try:
        pur = sess.query(RoleEntity).filter_by(
            rolName=role_name).one()
        return pur

    except NoResultFound:
        print "Unable to find row in find_role_by_role_name()"

    return None


def find_role_by_username_and_projectid(username, project_id):
    """ Fetch the role object for the specified username and project_id

    :rtype RoleEntity
    """
    try:
        user_id = find_auth_by_username(username).usrID
        return find_role_by_userid_and_projectid(user_id, project_id)
    except NoResultFound:
        print "Unable to find row in find_auth_by_username()"

    return None


def find_role_by_userid_and_projectid(user_id, project_id):
    """ Fetch the role object for the specified user_id and project_id

    :rtype RoleEntity
    """
    sess = app.db_session
    try:
        pur = sess.query(ProjectUserRoleEntity).filter_by(
            usrID=user_id, prjID=project_id).one()
        return pur.role

    except NoResultFound:
        print "Unable to find row in find_auth_by_username()"

    return None

"""
print "==========="
user = find_user_by_email('admin@example.com')
print user
print user.auth
print user.roles

auth = find_auth_by_username('admin')
print auth
print auth.user

role = find_role_by_username_and_projectid('admin', 2)
print role
"""
