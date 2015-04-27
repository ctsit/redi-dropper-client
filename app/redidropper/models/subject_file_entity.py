"""
ORM for RediDropper.SubjectFile table
"""

from redidropper.main import db
from redidropper.database.crud_mixin import CRUDMixin


class SubjectFileEntity(db.Model, CRUDMixin):

    """ Stores the file metadata """
    __tablename__ = 'SubjectFile'

    id = db.Column("sfID", db.Integer, primary_key=True)
    subject_id = db.Column("sbjID", db.Integer, db.ForeignKey('Subject.sbjID'),
                           nullable=False)
    event_id = db.Column("evtID", db.Integer, db.ForeignKey('Event.evtID'),
                         nullable=False)
    file_name = db.Column("sfFileName", db.String(255), nullable=False)
    file_check_sum = db.Column("sfFileCheckSum", db.String(32), nullable=False)
    uploaded_at = db.Column("sfUploadedAt", db.DateTime(), nullable=False,
                            server_default='0000-00-00 00:00:00')
    user_id = db.Column("usrID", db.Integer, db.ForeignKey('User.usrID'),
                        nullable=False)

    # @OneToOne
    subject = db.relationship('SubjectEntity', uselist=False, lazy='joined')
    event = db.relationship('EventEntity', uselist=False, lazy='joined')
    user = db.relationship('UserEntity', uselist=False, lazy='joined')

    def __repr__(self):
        return "<SubjectFileEntity (sfID: {0.id}, sbjID: {0.subject_id})>" \
            "usrID: {0.user_id}".format(self)
