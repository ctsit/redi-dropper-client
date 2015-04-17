"""
ORM for Role table
"""

from redidropper.main import db

ROLE_ADMIN = 'admin'
ROLE_TECHNICIAN = 'technician'

class RoleEntity(db.Model):
    """ Stores possible user roles """

    __tablename__ = 'Role'
    id = db.Column("rolID", db.Integer, primary_key=True)
    name = db.Column("rolName", db.String(255), nullable=False, unique=True)
    description = db.Column("rolDescription", db.String(255), nullable=False)


    def is_admin(self):
        """ helper for checking role """
        return ROLE_ADMIN == self.name


    def is_technician(self):
        """ helper for checking role """
        return ROLE_TECHNICIAN == self.name


    def __repr__(self):
        """ implements friendly representation """
        return "<RoleEntity (rolID: {}, rolName: {})>" \
            .format(self.id, self.name)
