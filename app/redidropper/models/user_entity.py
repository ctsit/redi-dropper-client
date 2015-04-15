"""
ORM for User table
"""

from flask_login import UserMixin as LoginUserMixin
from redidropper.main import db
from redidropper.utils import get_db_friendly_date_time, \
    dump_datetime


class UserEntity(db.Model, LoginUserMixin):
    """ Stores the basic information about the user.

    Implements the functions as required by:
        https://flask-login.readthedocs.org/en/latest/
    """
    visible_props = ['usrID', 'usrEmail', 'usrFirst', 'usrLast', 'usrMI', \
        'usrAddedAt', 'usrIsActive'
    ]

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


    def __init__(self, email, first='', last='', minitial='', is_active=1):
        """ Instantiate a UserEntity to be persisted """
        self.usrEmail = email
        self.usrFirst = first
        self.usrLast = last
        self.usrMI = minitial
        self.usrAddedAt = get_db_friendly_date_time()
        self.usrIsActive = is_active

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

    @property
    def to_visible(self):
        """
        Helper for exposing only "secure" class attributes as a dictionary
        """
        return dict( [(key, val) for key, val in self.__dict__.items() \
                if key in UserEntity.visible_props])

    #@property
    def serialize(self, project_id):
        """Return object data in easily serializeable format"""

        return {
            'usrID':    self.usrID,
            'usrEmail': self.usrEmail,
            'usrFirst': self.usrFirst,
            'usrLast':  self.usrLast,
            'usrMI':    self.usrMI,
            'usrAddedAt': dump_datetime(self.usrAddedAt),
            'usrIsActive': self.usrIsActive,
            'uathUsername': '' if self.auth is None else self.auth.uathUsername,
            'rolName': '' if self.role is None else self.role.rolName,
        }


    def __repr__(self):
        return "<UserEntity (usrID: {}, usrEmail: {})>" \
            .format(self.usrID, self.usrEmail)
