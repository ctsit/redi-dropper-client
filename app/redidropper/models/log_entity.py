"""
ORM for RediDropper.Log table
"""
# import datetime
from redidropper.database.crud_mixin import CRUDMixin
from redidropper.main import db
# from redidropper.models.log_type_entity import LogTypeEntity


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
    log_type = db.relationship(
        'LogTypeEntity',
        uselist=False,
        lazy='joined')
    web_session = db.relationship('WebSessionEntity',
                                  uselist=False,
                                  lazy='joined')

    def __repr__(self):
        """ Return a friendly object representation """
        return "<LogEntity(logID: {0.id}, "\
            "logtID: {0.type_id}" \
            "webID: {0.web_session_id}, "\
            "date_time: {0.date_time})>".format(self)
