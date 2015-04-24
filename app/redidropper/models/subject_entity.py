"""
ORM for RediDropper.Subject table
"""

from redidropper.main import db
from redidropper.database.crud_mixin import CRUDMixin


class SubjectEntity(db.Model, CRUDMixin):

    """ Stores the REDCap subject data """
    __tablename__ = 'Subject'

    id = db.Column("sbjID", db.Integer, primary_key=True)
    redcap_id = db.Column("sbjRedcapID", db.String(255), nullable=False,
                          unique=True)
    added_at = db.Column("usrAddedAt", db.DateTime(), nullable=False,
                         server_default='0000-00-00 00:00:00')
    last_checked_at = db.Column("sbjLastCheckedAt",
                                db.DateTime(),
                                nullable=False,
                                server_default='0000-00-00 00:00:00')
    was_deleted = db.Column("sbjWasDeleted", db.Boolean(), nullable=False,
                            server_default='0')

    # @OneToOne
    # user = db.relationship('UserEntity', uselist=False, lazy='joined')

    def __repr__(self):
        return """<SubjectEntity (sbjID: {0.id},
        sbjRedcapID: {0.redcap_id}, sbjAddedAt: {0.added_at})>""".format(self)
