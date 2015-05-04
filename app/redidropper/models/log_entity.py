import datetime

from redidropper.database.crud_mixin import CRUDMixin
from redidropper.main import db


class LogEntity(db.Model, CRUDMixin):
    __tablename__ = 'Log'

    # logID integer unsigned NOT NULL AUTO_INCREMENT,
    id = db.Column('logID', db.Integer, primary_key=True)
    # logtID integer unsigned NOT NULL,
    type_id = db.Column('logtID', db.Integer, db.ForeignKey('LogType.logtID'),
                        nullable=False),
    # logIP varchar(15) NOT NULL DEFAULT '',
    ip = db.Column('logIP', db.VARCHAR(15), nullable=False, default='')
    # webID integer unsigned NOT NULL,
    web_session_id = db.Column('webID', db.Integer,
                               db.ForeignKey('WebSession.webID'),
                               nullable=False)
    # logDateTime datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    date_time = db.Column('logDateTime', db.DateTime, nullable=False,
                          default=datetime.datetime(datetime.MINYEAR, 1, 1))
    # logDetails text NOT NULL,
    details = db.Column('logDetails', db.TEXT, nullable=False)

    # TODO: use "relationships" like...
    # type = db.relationship('LogTypeEntity', uselist=False)

    def __repr__(self):
        # TODO: finish __repr__ implementation
        return "<LogEntity(id='{0.id}',...)>".format(self)


class LogTypeEntity(db.Model, CRUDMixin):
    """
    CREATE TABLE LogType (
        logtID integer unsigned NOT NULL AUTO_INCREMENT,
        logtType varchar(255) NOT NULL,
        logtDescription text NOT NULL,
     PRIMARY KEY (logtID),
     UNIQUE KEY (logtType)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ;
    """
    __tablename__ = 'LogType'

    id = db.Column('logtID', db.Integer, primary_key=True)
    type = db.Column('logtType', db.VARCHAR(255), nullable=False)
    description = db.Column('logtDescription', db.Text, nullable=False)

    def __repr__(self):
        return ("<LogTypeEntity(id='{0.id}', type='{0.type'}, "
                "description='{0.description}')>".format(self))


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
    session_id = db.Column('webSessID', db.VARCHAR(255), nullable=False,
                           default='')
    user_id = db.Column('usrID', db.Integer, nullable=False, default=0)
    ip = db.Column('webIP', db.VARCHAR(15), nullable=False, default='')
    date_time = db.Column('webDateTime', db.DateTime, nullable=False,
                          default=datetime.datetime(datetime.MINYEAR, 1, 1))
    # TODO: use FK for uaID
    # user_agent_id = db.Column('uaID', db.Integer,
    #                          db.ForeignKey('UserAgent.uaID'),
    #                          nullable=False, default=0)
    user_agent_id = db.Column('uaID', db.Integer, nullable=False, default=0)

    def __repr__(self):
        # TODO: finish __repr__ implementation
        return "<WebSessionEntity(id='{0.id}',...)>".format(self)