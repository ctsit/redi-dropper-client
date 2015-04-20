"""
ORM for ProjectUserRole table
"""

from redidropper.main import db
from redidropper.models.project_entity import ProjectEntity
from redidropper.models.user_entity import UserEntity
from redidropper.models.role_entity import RoleEntity

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
    __table_args__ = (db.UniqueConstraint('prjID', 'usrID', name='prjID'), )


    def __init__(self, project_id, user_id, role_id):
        self.prjID = project_id
        self.usrID = user_id
        self.rolID = role_id


    def __repr__(self):
        return "<ProjectUserRoleEntity (\n\t" \
            "purID: {0.purID!r}, \n\t" \
            " {0.project}, \n\t" \
            " {0.user}, \n\t" \
            " {0.role}, \n" \
            ")>".format(self)
