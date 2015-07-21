"""
ORM for RediDropper.Subject table
"""

from redidropper.main import db
from redidropper import utils
from redidropper.database.crud_mixin import CRUDMixin


class SubjectEntity(db.Model, CRUDMixin):

    """ Stores the REDCap subject data """
    __tablename__ = 'Subject'

    id = db.Column("sbjID", db.Integer, primary_key=True)
    redcap_id = db.Column("sbjRedcapID", db.String(255), nullable=False,
                          unique=True)
    added_at = db.Column("sbjAddedAt", db.DateTime(), nullable=False,
                         server_default='0000-00-00 00:00:00')
    last_checked_at = db.Column("sbjLastCheckedAt",
                                db.DateTime(),
                                nullable=False,
                                server_default='0000-00-00 00:00:00')
    was_deleted = db.Column("sbjWasDeleted", db.Boolean(), nullable=False,
                            server_default='0')

    def __repr__(self):
        return """<SubjectEntity (sbjID: {0.id},
        sbjRedcapID: {0.redcap_id}, sbjAddedAt: {0.added_at})>""".format(self)

    @staticmethod
    def get_by_redcap_id(redcap_id):
        """ Search helper: WHERE redcap_id = 123"""
        subject = SubjectEntity.query.filter_by(redcap_id=redcap_id).first()
        print subject
        return subject

    def serialize(self):
        """Return object data for jsonification

        Note: There is some `residual jsx code` that expects the
            `events` array to be sent
        """
        return {
            'id': self.id,
            'redcap_id': self.redcap_id,
            'events': [],
            'added_at': utils.localize_est_datetime(self.added_at),
            'last_checked_at': utils.localize_est_datetime(
                self.last_checked_at),
            'was_deleted': self.was_deleted
        }
