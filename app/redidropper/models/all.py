"""
Goal: Store table models

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>

@see https://pythonhosted.org/Flask-SQLAlchemy/
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import TIMESTAMP
from flask_login import UserMixin as LoginUserMixin

#Base = declarative_base()

from redidropper.main import db

class ProjectEntity(db.Model):
    """ Stores details about projects """
    __tablename__ = 'Project'

    prjID = Column(Integer, primary_key=True)
    prjName = Column(String(255), nullable=False)
    prjUrlHost = Column(String(255), nullable=False)
    prjUrlPath = Column(String(255), nullable=False)
    prjApiKey = Column(String(255), nullable=False)
    prjUrlPath = Column(String(255), nullable=False)
    prjAddedAt = Column(DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    prjModifiedAt = Column(TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')

    __table_args__ = (UniqueConstraint('prjUrlHost', 'prjUrlPath'), )

    def __repr__(self):
        return "<ProjectEntity (prjID: {}, prjName: {}, prjUrlHost: {})>" \
            .format(self.prjID, self.prjName, self.prjUrlHost)


class UserAuthEntity(db.Model):
    """ Stores the username/password for the user """
    __tablename__ = 'UserAuth'

    uathID = Column(Integer, primary_key=True)
    usrID = Column(Integer, ForeignKey('User.usrID'), nullable=False)
    uathUsername = Column(String(255), nullable=False, unique=True)
    uathPassword = Column(String(255), nullable=False)
    uathPasswordResetToken = Column(String(255), nullable=False, \
            server_default='')
    uathEmailConfirmationToken = Column(String(255), nullable=False, \
            server_default='')
    uathModifiedAt = Column(TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')

    # @OneToOne
    user = relationship('UserEntity', uselist=False, lazy='joined')

    def __repr__(self):
        return "<UserAuthEntity (\n\t" \
                "authID: {0}, uathUsername: {1}, uathModifiedAt: {2}, \n\t" \
                "{3}\n)>" \
            .format(self.uathID, self.uathUsername, self.uathModifiedAt, \
                self.user)


class UserEntity(db.Model, LoginUserMixin):
    """ Stores the basic information about the user.

    Implements the functions as required by:
        https://flask-login.readthedocs.org/en/latest/
    """
    __tablename__ = 'User'
    usrID = Column(Integer, primary_key=True)
    usrEmail = Column(String(255), nullable=False, unique=True)
    usrFirst = Column(String(255), nullable=False)
    usrLast = Column(String(255), nullable=False)
    usrMI = Column(String(1), nullable=False)
    usrAddedAt = Column(DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    usrModifiedAt = Column(TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')
    usrEmailConfirmedAt = Column(DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    usrIsActive = Column(Boolean(), nullable=False, server_default='1')

    # @OneToOne
    auth = relationship('UserAuthEntity', uselist=False)

    # @OneToMany
    roles = relationship('RoleEntity', \
            secondary='ProjectUserRole', \
            backref=backref('user'))

    """
    `lazy` defines when SQLAlchemy will load the data from the database:
        'select' (which is the default) means that SQLAlchemy will load the data
        as necessary in one go using a standard select statement.
    'joined' tells SQLAlchemy to load the relationship in the same query as the
        parent using a JOIN statement.
    'subquery' works like 'joined' but instead SQLAlchemy will use a subquery.
    'dynamic' is special and useful if you have may items. Instead of loading
        the items SQLAlchemy will return another query object which you can
        further refine before loading them items. This is usually what you want
        if you expect more than a handful of items for this relationship.
    """

    project_roles = relationship('ProjectUserRoleEntity', \
                                lazy='joined')


    def __init__(self, usrEmail, usrFirst, usrLast, usrMI='', usrIsActive=1):
        """ Instantiate a UserEntity to be persisted """
        self.usrEmail = usrEmail
        self.usrFirst = usrFirst
        self.usrLast = usrLast
        self.usrMI = usrMI
        self.usrIsActive = usrIsActive

    def get_id(self):
        """ The id encrypted in the session """
        return unicode(self.usrID)

    def is_active(self):
        """ An user can be blocked by setting a flag in the database """
        return self.usrIsActive

    def is_anonymous(self):
        """ Flag instances of valid users """
        return False

    def is_authenticated(self):
        """ Returns True if the user is authenticated, i.e. they have provided
        valid credentials.
        (Only authenticated users will fulfill the criteria of login_required.)
        """
        return True

    def __repr__(self):
        return "<UserEntity (usrID: {}, usrEmail: {})>" \
            .format(self.usrID, self.usrEmail)


class RoleEntity(db.Model):
    """ Stores possible user roles """

    __tablename__ = 'Role'
    rolID = Column(Integer, primary_key=True)
    rolName = Column(String(255), nullable=False, unique=True)
    rolDescription = Column(String(255), nullable=False)

    def is_admin(self):
        return 'admin' == self.rolName

    def __repr__(self):
        return "<RoleEntity (rolID: {}, rolName: {})>" \
            .format(self.rolID, self.rolName)


class ProjectUserRoleEntity(db.Model):
    """ Stores the user's project roles """

    __tablename__ = 'ProjectUserRole'
    purID = Column(Integer, primary_key=True)
    prjID = Column(Integer, ForeignKey('Project.prjID', ondelete='CASCADE'), \
            nullable=False)
    usrID = Column(Integer, ForeignKey('User.usrID', ondelete='CASCADE'), \
            nullable=False)
    rolID = Column(Integer, ForeignKey('Role.rolID', ondelete='CASCADE'), \
            nullable=False)

    # @OneToOne
    role = relationship('RoleEntity', uselist=False)
    project = relationship('ProjectEntity', uselist=False)
    user = relationship('UserEntity', uselist=False)

    def get_id(self):
        return unicode(self.purID)

    # Don't allow more than one role for a specific user for a specific project
    __table_args__ = (UniqueConstraint('prjID', 'usrID', name='project_user'), )

    def __repr__(self):
        return "<ProjectUserRoleEntity (\n\t" \
            "purID: {0.purID!r}, \n\t" \
            " {1}, \n\t" \
            " {2}, \n\t" \
            " {3}, \n" \
            ")>".format(self, self.project, self.user, self.role)
