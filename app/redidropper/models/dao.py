"""
Goal: Implement the DAO

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound

from all import ProjectEntity
from all import UserEntity
from all import RoleEntity
from all import UserAuthEntity
from all import ProjectUserRoleEntity

def get_session():
    """
    Create a database session object
    @TODO: http://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session

    """
    user = 'redidropper'
    passwd = 'insecurepassword'
    host = 'localhost'
    db_name = 'RediDropper'

    engine = create_engine('mysql://{}:{}@{}/{}' \
            .format(user, passwd, host, db_name))
    Session = scoped_session(sessionmaker(bind=engine))
    sess = Session()
    return sess


def find_user_by_id(user_id):
    """ Fetch the user object using the primary key

    :rtype: UserEntity
    """
    sess = get_session()
    #user = User("test@test.com", "usrFirst", "usrLast")
    #sess.add(user)
    # sess.commit()
    try:
        user = sess.query(User).filter_by(usrID=user_id).one()
        return user
    except NoResultFound:
        print "Unable to find row in find_user_by_id()"

    return None


def find_user_by_email(email):
    """ Fetch the user object using the email unique key

    :rtype: UserEntity
    """
    sess = get_session()
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
    sess = get_session()

    try:
        auth = sess.query(UserAuthEntity).filter_by(
            uathUsername=username).one()
        return auth
    except NoResultFound:
        print "Unable to find row in find_auth_by_username()"

    return None


def find_role_by_username_and_projectid(username, project_id):
    """ Fetch the role object for the specified username and project_id

    :rtype RoleEntity
    """
    # translate the username into usrID
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
    sess = get_session()
    try:
        pur = sess.query(ProjectUserRoleEntity).filter_by(
            usrID=user_id, prjID=project_id).one()
        return pur.role

    except NoResultFound:
        print "Unable to find row in find_auth_by_username()"

    return None


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
#print role.users
