from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import select
#from redidropper.main import app, db

# Examples:
# ! http://www.pythoncentral.io/sqlalchemy-orm-examples/
# !! http://www.pythoncentral.io/sqlalchemy-expression-language-advanced/
# !!! http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#self-referential-many-to-many-relationship

# http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
# http://stackoverflow.com/questions/17972020/how-to-execute-raw-sql-in-sqlalchemy-flask-app
# http://www.dangtrinh.com/2013/06/sqlalchemy-python-module-with-mysql.html

# http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/declarative.html
# http://sqlalchemy.readthedocs.org/en/improve_toc/orm/join_conditions.html
# http://stackoverflow.com/questions/16028714/sqlalchemy-type-object-role-user-has-no-attribute-foreign-keys
# https://github.com/mitsuhiko/flask-sqlalchemy/issues/98
# http://version2beta.com/articles/migrating-from-mysql-to-postresql-using-sqlalchemy/


# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers-contacts-and-friends

Base = declarative_base()


class ProjectEntity(Base):
    """ Stores details about projects """
    __tablename__ = 'Project'

    prjID = Column(Integer, primary_key=True)
    prjName = Column(String(255), nullable=False)
    prjUrlHost = Column(String(255), nullable=False)
    prjUrlPath = Column(String(255), nullable=False)
    prjApiKey = Column(String(255), nullable=False)
    prjUrlPath = Column(String(255), nullable=False)
    prjAddedAt = Column(DateTime(), nullable=False,
        server_default='0000-00-00 00:00:00')
    prjModifiedAt = Column(TIMESTAMP(), nullable=False,
        server_default='CURRENT_TIMESTAMP')

    __table_args__ = (
            UniqueConstraint('prjUrlHost', 'prjUrlPath', name='host_path'), )

    def __repr__(self):
        return "<ProjectEntity (prjID: {}, prjName: {}, prjUrlHost: {})>" \
            .format(self.prjID, self.prjName, self.prjUrlHost)

class UserAuthEntity(Base):
    """ Stores the username/password for the user """
    __tablename__ = 'UserAuth'

    uathID = Column(Integer, primary_key=True)
    usrID = Column(Integer, ForeignKey('User.usrID'), nullable=False)
    uathUsername = Column(String(255), nullable=False, unique=True)
    uathPassword = Column(String(255), nullable=False)
    uathPasswordResetToken = Column(String(255), nullable=False,
        server_default='')
    uathEmailConfirmationToken = Column(String(255), nullable=False,
        server_default='')
    uathModifiedAt = Column(TIMESTAMP(), nullable=False,
        server_default='CURRENT_TIMESTAMP')

    # @OneToOne
    user = relationship('UserEntity', uselist=False)

    def __repr__(self):
        return "<UserAuthEntity (usrID: {}, uathUsername: {}, uathModifiedAt: {})>" \
            .format(self.usrID, self.uathUsername, self.uathModifiedAt)


class UserEntity(Base):
    """ Stores the basic information about the user """
    __tablename__ = 'User'
    usrID = Column(Integer, primary_key=True)
    usrEmail = Column(String(255), nullable=False, unique=True)
    usrFirst = Column(String(255), nullable=False)
    usrLast = Column(String(255), nullable=False)
    usrMI = Column(String(1), nullable=False)
    usrAddedAt = Column(DateTime(), nullable=False,
        server_default='0000-00-00 00:00:00')
    usrModifiedAt = Column(TIMESTAMP(), nullable=False,
        server_default='CURRENT_TIMESTAMP')
    usrEmailConfirmedAt = Column(DateTime(), nullable=False,
        server_default='0000-00-00 00:00:00')
    usrIsActive = Column(Boolean(), nullable=False, server_default='1')

    # @OneToOne
    user_auth = relationship('UserAuthEntity', uselist=False)

    # @OneToMany
    roles = relationship(
            'RoleEntity',
            secondary='ProjectUserRole',
            backref=backref('user'))

    def __init__(self, usrEmail, usrFirst, usrLast, usrMI=''):
        self.usrEmail = usrEmail
        self.usrFirst = usrFirst
        self.usrLast = usrLast
        self.usrMI = usrMI

    def __repr__(self):
        return "<UserEntity (usrID: {}, usrEmail: {})>" \
            .format(self.usrID, self.usrEmail)


class RoleEntity(Base):
    """ Stores possible user roles """
    __tablename__ = 'Role'
    rolID = Column(Integer, primary_key=True)
    rolName = Column(String(255), nullable=False, unique=True)
    rolDescription = Column(String(255), nullable=False)

    users = relationship(
        'UserEntity',
        secondary='ProjectUserRole',
        backref=backref('role')
    )

    def __repr__(self):
        return "<RoleEntity (rolID: {}, rolName: {}, rolDescription: {})>" \
            .format(self.rolID, self.rolName, self.rolDescription)

class ProjectUserRoleEntity(Base):
    """ Stores the user's project roles """

    __tablename__ = 'ProjectUserRole'
    purID = Column(Integer, primary_key=True)
    prjID = Column(Integer, ForeignKey('Project.prjID', ondelete='CASCADE'),
            nullable=False)
    usrID = Column(Integer, ForeignKey('User.usrID', ondelete='CASCADE'),
           nullable=False)
    rolID = Column(Integer, ForeignKey('Role.rolID', ondelete='CASCADE'),
            nullable=False)

    # Don't allow more than one role for a specific user for a specific project
    __table_args__ = (
            UniqueConstraint('prjID', 'usrID', name='project_user'), )


    # @OneToOne
    #user = relationship('User', uselist=False)
    #project = relationship('Project', uselist=False)
    #role = relationship('Role', uselist=False)

    def __repr__(self):
        #return "<ProjectUserRole(purID: {}, prjID: {}, usrID: {}, rolID: {})>" \
        #    .format(self.purID, self.prjID, self.usrID, self.rolID)
        return "<ProjectUserRoleEntity (purID: {}, usrID: {}, rolID: {})>" \
            .format(self.purID, self.usrID, self.rolID)


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
    user = sess.query(User).filter_by(usrID=user_id).one()
    return user


def find_user_by_email(email):
    """ Fetch the user object using the email unique key

    :rtype: UserEntity
    """
    sess = get_session()
    user = sess.query(UserEntity).filter_by(usrEmail=email).one()
    return user


def find_auth_by_username(username):
    """ Fetch the auth object for the specified username

    :rtype UserAuthEntity
    """
    sess = get_session()
    auth = sess.query(UserAuthEntity).filter_by(
        uathUsername=username).one()
    return auth


def find_role_by_username_and_projectid(username, project_id):
    """ Fetch the role object for the specified username and project_id

    :rtype RoleEntity
    """
    # translate the username into usrID
    user_id = find_auth_by_username(username).usrID
    return find_role_by_userid_and_projectid(user_id, project_id)


def find_role_by_userid_and_projectid(user_id, project_id):
    """ Fetch the role object for the specified user_id and project_id

    :rtype RoleEntity
    """

    sess = get_session()
    pur = sess.query(ProjectUserRoleEntity).filter_by(
        usrID=user_id, prjID=project_id).one()
    return pur

print "==========="
user = find_user_by_email('admin@example.com')
print user.roles

auth = find_auth_by_username('admin')
print auth

pur = find_role_by_username_and_projectid('admin', 1)
print pur
