"""
ORM for RediDropper.LogType table
"""
from redidropper.database.crud_mixin import CRUDMixin
from redidropper.main import db


class LogTypeEntity(db.Model, CRUDMixin):

    """ Stores types of logs """
    __tablename__ = 'LogType'

    id = db.Column('logtID', db.Integer, primary_key=True)
    type = db.Column('logtType', db.String(255), nullable=False)
    description = db.Column('logtDescription', db.Text, nullable=False)

    def __repr__(self):
        """ Return a friendly object representation """
        return ("<LogTypeEntity(id: {0.id}, "\
                "logtType: {0.type}, "
                "logtDescription: {0.description})>"
                .format(self))
