"""
ORM for Role table
"""

from redidropper.main import db

ROLE_ADMIN = 'admin'
ROLE_TECHNICIAN = 'technician'

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


