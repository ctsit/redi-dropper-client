"""
ORM for Role table
"""

# from flask_security import RoleMixin
from redidropper.main import db
from redidropper.database.crud_mixin import CRUDMixin

ROLE_ADMIN = 'admin'
ROLE_TECHNICIAN = 'technician'
ROLE_RESEARCHER_ONE = 'researcher_one'
ROLE_RESEARCHER_TWO = 'researcher_two'

class RoleEntity(db.Model, CRUDMixin):  # RoleMixin
    """ Stores possible user roles """
    __tablename__ = 'Role'

    id = db.Column("rolID", db.Integer, primary_key=True)
    name = db.Column("rolName", db.String(255), nullable=False, unique=True)
    description = db.Column("rolDescription", db.String(255), nullable=False)

    def __repr__(self):
        """ implements friendly representation """
        return "<RoleEntity (rolID: {0.id}, rolName: {0.name})>" \
            .format(self)
