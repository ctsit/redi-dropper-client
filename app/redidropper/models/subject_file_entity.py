"""
ORM for RediDropper.SubjectFile table
"""
import os
from redidropper.main import app, db
from redidropper import utils
from redidropper.database.crud_mixin import CRUDMixin

logger = app.logger

class SubjectFileEntity(db.Model, CRUDMixin):
    """ Stores the uploaded file metadata """
    __tablename__ = 'SubjectFile'

    id = db.Column("sfID", db.Integer, primary_key=True)
    subject_id = db.Column("sbjID", db.Integer, db.ForeignKey('Subject.sbjID'),
                           nullable=False)
    event_id = db.Column("evtID", db.Integer, db.ForeignKey('Event.evtID'),
                         nullable=False)
    file_name = db.Column("sfFileName", db.String(255), nullable=False)
    file_check_sum = db.Column("sfFileCheckSum", db.String(32), nullable=False)
    file_size = db.Column("sfFileSize", db.String(255), nullable=False)
    file_type = db.Column("sfFileType", db.String(255), nullable=False)
    uploaded_at = db.Column("sfUploadedAt", db.DateTime, nullable=False,
                            server_default='0000-00-00 00:00:00')
    user_id = db.Column("usrID", db.Integer, db.ForeignKey('User.usrID'),
                        nullable=False)

    # @OneToOne
    subject = db.relationship('SubjectEntity', uselist=False, lazy='joined')
    event = db.relationship('EventEntity', uselist=False, lazy='joined')
    user = db.relationship('UserEntity', uselist=False, lazy='joined')

    def create_folder(self, directory):
        """
        Create folder if it does not exist
        """
        success = True

        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as exc:
                print "Failed due: {}".format(exc)
                success = False
        return success

    @classmethod
    def get_convention_file_name(cls, date_and_time, subject_id, file_name):
        """
        Concatenate the pieces to obtain a fiendly file name.

        @TODO: check if we need to need the "site ID" and
            how to obtain it.

        Original convention:
            20120101_0123_SiteID_A_SubjectID_B_Sequence123_xyz.jpg

        Actual implementation (does not keep track of sequences):
            20120101_0123_site_subject_B_xyz.jpg
        """
        date_part = date_and_time.strftime("%Y%m%d")
        time_part = date_and_time.strftime("%H%M")

        file_convention = "{}_{}_site_subject_{}_{}".format(
            date_part,
            time_part,
            subject_id,
            file_name)
        return file_convention

    def get_full_path(self, prefix):
        """
        Build the full path using the database info and the prefix
        @TODO: implement the naming convention

        20120101_0123_SiteIDA_SubjectIDB_Sequence123_xyz.jpg
        """
        subject_dir = os.path.join(
            prefix, "subject_{}".format(self.subject.redcap_id))
        success = self.create_folder(subject_dir)
        assert success

        file_convention = SubjectFileEntity.get_convention_file_name(
            self.uploaded_at,
            self.subject.redcap_id,
            self.file_name)
        full_path = os.path.join(subject_dir, file_convention)
        return full_path

    def __repr__(self):
        """ Return a friendly object representation """
        return "<SubjectFileEntity (sfID: {0.id}, sbjID: {0.subject_id}, " \
            "usrID: {0.user_id}, sfFileName: {0.file_name}>)".format(self)

    def serialize(self):
        """Return object data for jsonification """
        # @TODO: add information about download counts
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_check_sum': self.file_check_sum,
            'file_size': self.file_size,
            'file_type': self.file_type,  
            'uploaded_at': utils.localize_est_datetime(self.uploaded_at),
            'subject_id': self.subject_id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'user_name': self.user.get_name()
        }
