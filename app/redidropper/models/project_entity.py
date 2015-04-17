"""
ORM for Project table
"""

from redidropper.main import db

class ProjectEntity(db.Model):
    """ Stores details about projects """
    __tablename__ = 'Project'

    prjID = db.Column(db.Integer, primary_key=True)
    prjName = db.Column(db.String(255), nullable=False)
    prjUrlHost = db.Column(db.String(255), nullable=False)
    prjUrlPath = db.Column(db.String(255), nullable=False)
    prjApiKey = db.Column(db.String(255), nullable=False)
    prjAddedAt = db.Column(db.DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    prjModifiedAt = db.Column(db.TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')

    __table_args__ = (db.UniqueConstraint('prjUrlHost', 'prjUrlPath'), )


    def __init__(self, name=None, host=None, path=None, \
            api_key=None, added=None):
        self.prjName = name
        self.prjUrlHost = host
        self.prjUrlPath = path
        self.prjApiKey = api_key
        self.prjAddedAt = added


    def __repr__(self):
        return "<ProjectEntity (prjID: {}, prjName: {}, prjUrlHost: {})>" \
            .format(self.prjID, self.prjName, self.prjUrlHost)
