"""
ORM for RediDropper.WebSession table
"""
import datetime
from redidropper.database.crud_mixin import CRUDMixin
from redidropper.main import db


class WebSessionEntity(db.Model, CRUDMixin):
    """
    CREATE TABLE WebSession (
        webID integer unsigned NOT NULL AUTO_INCREMENT,
        webSessID varchar(255) NOT NULL DEFAULT '',
        usrID integer unsigned NOT NULL DEFAULT '0',
        webIP varchar(15) NOT NULL DEFAULT '',
        webDateTime datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
        uaID integer unsigned NOT NULL DEFAULT '0',
     PRIMARY KEY (webID),
     KEY (usrID),
     KEY (webDateTime),
     KEY (uaID),
     CONSTRAINT `fk_WebSession_uaID` FOREIGN KEY (uaID) REFERENCES UserAgent (uaID)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ;
    """
    __tablename__ = 'WebSession'

    id = db.Column('webID', db.Integer, primary_key=True)
    session_id = db.Column('webSessID', db.String(255), nullable=False,
                           default='')
    user_id = db.Column('usrID', db.Integer, nullable=False, default=0)
    ip = db.Column('webIP', db.String(15), nullable=False, default='')
    date_time = db.Column('webDateTime', db.DateTime, nullable=False,
                          default=datetime.datetime(datetime.MINYEAR, 1, 1))
    # TODO: use FK for uaID
    # user_agent_id = db.Column('uaID', db.Integer,
    #                          db.ForeignKey('UserAgent.uaID'),
    #                          nullable=False, default=0)
    user_agent_id = db.Column('uaID', db.Integer, nullable=False, default=0)

    def __repr__(self):
        """ Return a friendly object representation """
        return "<WebSessionEntity (webID: '{0.id}', webSessID: {0.session_id},"\
        " usrID: {0.user_id}, webIP: {0.ip})>".format(self)
