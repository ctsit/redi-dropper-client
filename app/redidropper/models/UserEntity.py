from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

#from redidropper.main import app, db

# Examples:
# http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
# http://stackoverflow.com/questions/17972020/how-to-execute-raw-sql-in-sqlalchemy-flask-app
# http://www.dangtrinh.com/2013/06/sqlalchemy-python-module-with-mysql.html
# http://www.pythoncentral.io/sqlalchemy-orm-examples/

# http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/declarative.html
# http://sqlalchemy.readthedocs.org/en/improve_toc/orm/join_conditions.html
# https://github.com/mitsuhiko/flask-sqlalchemy/issues/98

Base = declarative_base()

class Role(Base):
    """ Stores possible user roles """
    __tablename__ = 'Role'

    rolID = Column(Integer, primary_key=True)
    rolName = Column(String(255), nullable=False, unique=True)
    rolDescription = Column(String(255), nullable=False)

    def __repr__(self):
        return "<Role (rolID: {}, rolName: {}, rolDescription: {})>" \
            .format(self.rolID, self.rolName, self.rolDescription)


class Project(Base):
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
        return "<Project (prjID: {}, prjName: {}, prjUrlHost: {})>" \
            .format(self.prjID, self.prjName, self.prjUrlHost)


class User(Base):
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
    user_auth = relationship('UserAuth', uselist=False)

    # @OneToMany
    #roles = relationship('Role',
    #    # secondary='Project_User_Role',
    #    secondary='project_user_role',
    #    backref=backref('role', lazy='dynamic'))
    #project_roles = relationship('ProjectUserRole', backref='user_roles')

    def __init__(self, usrEmail, usrFirst, usrLast):
        self.usrEmail = usrEmail
        self.usrFirst = usrFirst
        self.usrLast = usrLast

    def __repr__(self):
        return "<User (usrID: {}, usrEmail: {})>" \
            .format(self.usrID, self.usrEmail)


class UserAuth(Base):
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
    user = relationship('User', uselist=False)
    #user = relationship(User, backref='user_authorization')

    def __repr__(self):
        return "<UserAuth(usrID: {}, uathUsername: {}, uathModifiedAt: {})>" \
            .format(self.usrID, self.uathUsername, self.uathModifiedAt)


    """
+-------+----------------------+------+-----+---------+----------------+
| Field | Type                 | Null | Key | Default | Extra          |
+-------+----------------------+------+-----+---------+----------------+
| purID | int(10) unsigned     | NO   | PRI | NULL    | auto_increment |
| prjID | smallint(5) unsigned | NO   | MUL | NULL    |                |
| usrID | int(10) unsigned     | NO   | MUL | NULL    |                |
| rolID | smallint(5) unsigned | NO   | MUL | NULL    |                |
+-------+----------------------+------+-----+---------+----------------+
    """


class ProjectUserRole(Base):
    """ Stores the user's project roles """
    # InvalidRequestError: On relationship ProjectUserRole.User, 'dynamic' loaders cannot be used with many-to-one/one-to-one relationships and/or uselist=False
    __tablename__ = 'ProjectUserRole'

    purID = Column(Integer, primary_key=True)
    prjID = Column(Integer, ForeignKey('Project.prjID', ondelete='CASCADE'), nullable=False)
    usrID = Column(Integer, ForeignKey('User.usrID', ondelete='CASCADE'), nullable=False)
    rolID = Column(Integer, ForeignKey('Role.rolID', ondelete='CASCADE'), nullable=False)

    # @OneToOne
    user = relationship('User', uselist=False)
    project = relationship('Project', uselist=False)
    role = relationship('Role', uselist=False)

    def __repr__(self):
        return "<ProjectUserRole(purID: {}, prjID: {}, usrID: {}, rolID: {})>" \
            .format(self.purID, self.prjID, self.usrID, self.rolID)


def get_session():
    """
    Create a database session object
    @TODO: http://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session

    """
    user = 'redidropper'
    passwd = 'insecurepassword'
    host = 'localhost'
    db_name = 'RediDropper'

    engine = create_engine('mysql://{}:{}@{}/{}'.format(user, passwd, host, db_name))
    Session = scoped_session(sessionmaker(bind=engine))
    sess = Session()
    return sess


def find_user_by_id(id):
    """ Fetch a user from the db using the primary key """
    sess = get_session()
    #user = User("test@test.com", "usrFirst", "usrLast")
    #sess.add(user)
    # sess.commit()
    users = sess.query(User).filter_by(usrID=id)
    #all_users = sess.query(User).all()
    return users[0]


def find_user_by_email(email):
    """ Fetch a user from the db using the email unique key """
    sess = get_session()
    users = sess.query(User).filter_by(usrEmail=email)
    return users[0]


def find_userauth_by_username(username):
    sess = get_session()
    auths = sess.query(UserAuth).filter_by(uathUsername=username)
    return auths[0]


user = find_user_by_email('admin@example.com')
print user

auth = find_userauth_by_username('admin')
print auth
