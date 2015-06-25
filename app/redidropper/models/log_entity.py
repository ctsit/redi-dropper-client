"""
ORM for RediDropper.Log table
"""
# import datetime
import datetime
from redidropper.database.crud_mixin import CRUDMixin
from redidropper.main import db
from redidropper.models.log_type_entity import LogTypeEntity
from redidropper.models.web_session_entity import WebSessionEntity


class LogEntity(db.Model, CRUDMixin):

    """ Keep track of important user actions """
    __tablename__ = 'Log'

    id = db.Column('logID', db.Integer, primary_key=True)
    type_id = db.Column('logtID', db.Integer,
                        db.ForeignKey('LogType.logtID'),
                        nullable=False)
    web_session_id = db.Column('webID', db.Integer,
                               db.ForeignKey('WebSession.webID'),
                               nullable=False)
    date_time = db.Column('logDateTime', db.DateTime, nullable=False,
                          server_default='0000-00-00 00:00:00')
    # datetime.datetime(datetime.MINYEAR, 1, 1))
    details = db.Column('logDetails', db.Text, nullable=False)

    # @OneToOne
    log_type = db.relationship(LogTypeEntity, uselist=False, lazy='joined')
    web_session = db.relationship(WebSessionEntity, uselist=False,
                                  lazy='joined')

    @staticmethod
    def _log(log_type, session_id, details=''):
        lt = LogTypeEntity.query.filter_by(type=log_type).one()
        LogEntity.create(log_type=lt,
                         date_time=datetime.datetime.now(),
                         details=details,
                         web_session=WebSessionEntity.get(session_id))

    @staticmethod
    def file_downloaded(session_id, details=''):
        LogEntity._log('file_downloaded', session_id, details)

    @staticmethod
    def file_uploaded(session_id, details=''):
        LogEntity._log('file_uploaded', session_id, details)

    @staticmethod
    def logout(session_id, details=''):
        LogEntity._log('logout', session_id, details)

    @staticmethod
    def login(session_id, details='', successful=True):
        if successful:
            LogEntity._log('login', session_id, details)
        else:
            LogEntity._log('login_error', session_id, details)

    @staticmethod
    def account_created(session_id, details=''):
        LogEntity._log('account_created', session_id, details)

    @staticmethod
    def account_modified(session_id, details=''):
        LogEntity._log('account_modified', session_id, details)

    def __repr__(self):
        """ Return a friendly object representation """
        return "<LogEntity(logID: {0.id}, "\
            "logtID: {0.type_id}" \
            "webID: {0.web_session_id}, "\
            "date_time: {0.date_time})>".format(self)
