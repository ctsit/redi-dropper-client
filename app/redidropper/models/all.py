"""
Goal: Store table models

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>

@see https://pythonhosted.org/Flask-SQLAlchemy/
"""

from flask_login import UserMixin as LoginUserMixin
from redidropper.main import db
#Base = declarative_base()

ROLE_ADMIN = 'admin'
ROLE_TECHNICIAN = 'technician'

class ProjectEntity(db.Model):
    """ Stores details about projects """
    __tablename__ = 'Project'

    prjID = db.Column(db.Integer, primary_key=True)
    prjName = db.Column(db.String(255), nullable=False)
    prjUrlHost = db.Column(db.String(255), nullable=False)
    prjUrlPath = db.Column(db.String(255), nullable=False)
    prjApiKey = db.Column(db.String(255), nullable=False)
    prjUrlPath = db.Column(db.String(255), nullable=False)
    prjAddedAt = db.Column(db.DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    prjModifiedAt = db.Column(db.TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')

    __table_args__ = (db.UniqueConstraint('prjUrlHost', 'prjUrlPath'), )

    def __repr__(self):
        return "<ProjectEntity (prjID: {}, prjName: {}, prjUrlHost: {})>" \
            .format(self.prjID, self.prjName, self.prjUrlHost)


class UserAuthEntity(db.Model):
    """ Stores the username/password for the user """
    __tablename__ = 'UserAuth'

    uathID = db.Column(db.Integer, primary_key=True)
    usrID = db.Column(db.Integer, db.ForeignKey('User.usrID'), nullable=False)
    uathUsername = db.Column(db.String(255), nullable=False, unique=True)
    uathSalt = db.Column(db.String(255), nullable=False)
    uathPassword = db.Column(db.String(255), nullable=False)
    uathPasswordResetToken = db.Column(db.String(255), nullable=False, \
            server_default='')
    uathEmailConfirmationToken = db.Column(db.String(255), nullable=False, \
            server_default='')
    uathModifiedAt = db.Column(db.TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')

    # @OneToOne
    user = db.relationship('UserEntity', uselist=False, lazy='joined')


    def __init__(self, usrID=None, uathUsername=None, uathSalt=None, uathPassword=None):
        """ Set the manadatory fields """
        self.usrID = usrID
        self.uathUsername = uathUsername
        self.uathSalt = 'Sample salt'
        self.uathPassword = 'password'


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
    usrID = db.Column(db.Integer, primary_key=True)
    usrEmail = db.Column(db.String(255), nullable=False, unique=True)
    usrFirst = db.Column(db.String(255), nullable=False)
    usrLast = db.Column(db.String(255), nullable=False)
    usrMI = db.Column(db.String(1), nullable=False)
    usrAddedAt = db.Column(db.DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    usrModifiedAt = db.Column(db.TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')
    usrEmailConfirmedAt = db.Column(db.DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    usrIsActive = db.Column(db.Boolean(), nullable=False, server_default='1')

    # @OneToOne
    auth = db.relationship('UserAuthEntity', uselist=False)

    # @OneToMany
    roles = db.relationship('RoleEntity', \
            secondary='ProjectUserRole', \
            backref=db.backref('user'))

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

    project_roles = db.relationship('ProjectUserRoleEntity', \
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
    rolID = db.Column(db.Integer, primary_key=True)
    rolName = db.Column(db.String(255), nullable=False, unique=True)
    rolDescription = db.Column(db.String(255), nullable=False)

    def is_admin(self):
        """ helper for checking role """
        return ROLE_ADMIN == self.rolName


    def is_technician(self):
        """ helper for checking role """
        return ROLE_TECHNICIAN == self.rolName


    def __repr__(self):
        """ implements friendly representation """
        return "<RoleEntity (rolID: {}, rolName: {})>" \
            .format(self.rolID, self.rolName)


class ProjectUserRoleEntity(db.Model):
    """ Stores the user's project roles """

    __tablename__ = 'ProjectUserRole'
    purID = db.Column(db.Integer, primary_key=True)
    prjID = db.Column(db.Integer, db.ForeignKey('Project.prjID', \
            ondelete='CASCADE'), nullable=False)
    usrID = db.Column(db.Integer, db.ForeignKey('User.usrID', \
            ondelete='CASCADE'), nullable=False)
    rolID = db.Column(db.Integer, db.ForeignKey('Role.rolID', \
            ondelete='CASCADE'), nullable=False)

    # @OneToOne
    role = db.relationship('RoleEntity', uselist=False)
    project = db.relationship('ProjectEntity', uselist=False)
    user = db.relationship('UserEntity', uselist=False)

    def get_id(self):
        """ return the unicode of the primary key value """
        return unicode(self.purID)

    # Don't allow more than one role for a specific user for a specific project
    __table_args__ = (db.UniqueConstraint('prjID', 'usrID', name='project_user'), )

    def __repr__(self):
        return "<ProjectUserRoleEntity (\n\t" \
            "purID: {0.purID!r}, \n\t" \
            " {0.project}, \n\t" \
            " {0.user}, \n\t" \
            " {0.role}, \n" \
            ")>".format(self)
