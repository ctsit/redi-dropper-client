"""
ORM for RediDropper.Subject table
"""

from redidropper.main import db
from redidropper.utils import dump_datetime
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

    # @OneToOne
    # user = db.relationship('UserEntity', uselist=False, lazy='joined')

    def __repr__(self):
        return """<SubjectEntity (sbjID: {0.id},
        sbjRedcapID: {0.redcap_id}, sbjAddedAt: {0.added_at})>""".format(self)

    def serialize(self):
        """Return object data for jsonification"""

        return {
            'id': self.id,
            'events': [],
            'events_dummy': [{'event_id': '1', 'event_files': '1'}],
            # 'files': [f.name for f in self.files],
            'added_at': dump_datetime(self.added_at),
            'last_checked_at': dump_datetime(self.last_checked_at),
            'was_deleted': self.was_deleted
        }
