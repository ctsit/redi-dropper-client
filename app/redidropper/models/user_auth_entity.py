"""
ORM for RediDropper.UserAuth table
"""

from redidropper.main import db


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


    def __init__(self, user_id, username, salt=None, password=None, \
            password_token=None, email_token=None):
        """ Set the manadatory fields """
        self.usrID = user_id
        self.uathUsername = username
        self.uathSalt = salt
        self.uathPassword = password
        self.uathPasswordResetToken = password_token
        self.uathEmailConfirmationToken = email_token


    def __repr__(self):
        return "<UserAuthEntity (\n\t" \
                "authID: {0}, uathUsername: {1}, uathModifiedAt: {2}, \n\t" \
                "{3}\n)>" \
            .format(self.uathID, self.uathUsername, self.uathModifiedAt, \
                self.user)
