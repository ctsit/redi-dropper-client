"""
ORM for Project table
"""

from redidropper.main import db
from redidropper.database.crud_mixin import CRUDMixin

class ProjectEntity(db.Model, CRUDMixin):
    """ Stores details about projects """
    __tablename__ = 'Project'

    # pylint: disable=bad-whitespace, no-self-use
    id          = db.Column('prjID', db.Integer, primary_key=True)
    name        = db.Column('prjName', db.String(255), nullable=False)
    url_host    = db.Column('prjUrlHost', db.String(255), nullable=False)
    url_path    = db.Column('prjUrlPath', db.String(255), nullable=False)
    api_key     = db.Column('prjApiKey', db.String(255), nullable=False)
    added_at    = db.Column('prjAddedAt', db.DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    modified_at = db.Column('prjModifiedAt', db.TIMESTAMP(), nullable=False)

    __table_args__ = (db.UniqueConstraint('prjUrlHost', 'prjUrlPath'), )


    def __repr__(self):
        return "<ProjectEntity (prjID: {}, prjName: {}, prjUrlHost: {})>" \
            .format(self.id, self.name, self.url_host)
