"""
ORM for RediDropper.SubjectFile table
"""
import os
from redidropper.main import db
from redidropper.utils import dump_datetime
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
    file_size = db.Column("sfFileSize", db.String(255), nullable=False)
    uploaded_at = db.Column("sfUploadedAt", db.DateTime(), nullable=False,
                            server_default='0000-00-00 00:00:00')
    user_id = db.Column("usrID", db.Integer, db.ForeignKey('User.usrID'),
                        nullable=False)

    # @OneToOne
    subject = db.relationship('SubjectEntity', uselist=False, lazy='joined')
    event = db.relationship('EventEntity', uselist=False, lazy='joined')
    user = db.relationship('UserEntity', uselist=False, lazy='joined')

    @classmethod
    def create_folder(self, prefix):
        """
        Create folder prefix/subject_id if it does not exist
        """
        directory = os.path.join(prefix, self.subject_id)
        print "dir: " + directory

        if not os.path.exists(directory):
            try:
                os.makedirs(directory)

                return directory
            except Exception as exc:
                print "Failed due: {}".format(exc)

    def get_full_path(self, prefix):
        """
        Build the full path using the database info and the prefix
        @TODO: implement the naming convention

        20120101_0123_SiteIDA_SubjectIDB_Sequence123_xyz.jpg
        """
        subject_dir = SubjectFileEntity.create_folder(prefix)
        assert subject_dir is not None

        when_date = '20150101'
        when_time = '0102'
        sequence = '1'
        file_convention = "{}_{}_site_{}_{}_{}".format(
            when_date, when_time, self.subject_id, sequence, self.file_name)

        return os.path.join(subject_dir, file_convention)

    def __repr__(self):
        return "<SubjectFileEntity (sfID: {0.id}, sbjID: {0.subject_id})>" \
            "usrID: {0.user_id}".format(self)

    def serialize(self):
        """Return object data for jsonification """

        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_check_sum': self.file_check_sum,
            'file_size': self.file_size,
            'uploaded_at': dump_datetime(self.uploaded_at),
            'subject_id': self.subject_id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'user_name': self.user.get_name(),
            # 'subject': self.subject.serialize(),
            # 'event': self.event.serialize(),
            # 'user': self.user.serialize(),
        }
