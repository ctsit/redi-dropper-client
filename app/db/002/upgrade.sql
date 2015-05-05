
USE RediDropper;

INSERT INTO Version (verID, verInfo)
    VALUES('002', 'Create tables: User, Role, UserRole, Subject, SubjectFile, UserAgent, WebSession, LogType, Log, Event')
;


-- http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html

-- Store user's personal info
-- usrPasswordResetToken varchar(255) NOT NULL DEFAULT '',
-- usrEmailConfirmationToken varchar(255) NOT NULL DEFAULT '',

CREATE TABLE User (
    usrID integer unsigned NOT NULL AUTO_INCREMENT,
    usrEmail varchar(255) NOT NULL DEFAULT '',
    usrFirst varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    usrLast varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    usrMI char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    usrAddedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    usrModifiedAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usrEmailConfirmedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    usrIsActive tinyint NOT NULL DEFAULT 1,
    usrAccessExpiresAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    usrPasswordHash varchar(255) NOT NULL DEFAULT '',
 PRIMARY KEY (usrID),
 UNIQUE KEY (usrEmail),
 KEY (usrFirst, usrLast),
 KEY (usrAddedAt),
 KEY (usrModifiedAt),
 KEY (usrEmailConfirmedAt),
 KEY(usrAccessExpiresAt)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

-- Store possible roles
CREATE TABLE Role (
    rolID smallint unsigned NOT NULL AUTO_INCREMENT,
    rolName varchar(255) NOT NULL,
    rolDescription varchar(255) NOT NULL,
 PRIMARY KEY (rolID),
 UNIQUE KEY (rolName)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

-- Store user roles mapping
CREATE TABLE UserRole (
    urID integer unsigned NOT NULL AUTO_INCREMENT,
    usrID integer unsigned NOT NULL,
    rolID smallint unsigned NOT NULL,
    urAddedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
 PRIMARY KEY (urID),
 CONSTRAINT `fk_User_usrID` FOREIGN KEY (usrID) REFERENCES User (usrID) ON DELETE CASCADE,
 CONSTRAINT `fk_UserRole_rolID` FOREIGN KEY (rolID) REFERENCES Role (rolID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

-- show active users but does not filter out the ones with usrAccessExpiresAt < NOW()
CREATE
    ALGORITHM=UNDEFINED
    DEFINER=`redidropper`@`localhost`
    VIEW `user_role_view`
AS
SELECT
    usrID, usrEmail, rolID, rolName, urAddedAt, usrAccessExpiresAt
FROM
    User
    JOIN UserRole USING (usrID)
    JOIN Role USING (rolID)
WHERE
    usrIsActive
;


CREATE TABLE Subject (
    sbjID int(10) unsigned NOT NULL AUTO_INCREMENT,
    sbjRedcapID varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    sbjAddedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    sbjLastCheckedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    sbjWasDeleted tinyint NOT NULL DEFAULT 0,
 PRIMARY KEY (sbjID),
 UNIQUE KEY(sbjRedcapID),
 KEY (sbjAddedAt),
 KEY(sbjLastCheckedAt)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE Event (
    evtID integer unsigned NOT NULL AUTO_INCREMENT,
    evtRedcapArm varchar(255) NOT NULL,
    evtRedcapEvent varchar(255) NOT NULL,
    evtAddedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
 PRIMARY KEY (evtID),
 UNIQUE KEY (evtRedcapArm, evtRedcapEvent),
 KEY (evtRedcapEvent),
 KEY (evtAddedAt)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE SubjectFile (
    sfID int(10) unsigned NOT NULL AUTO_INCREMENT,
    sbjID int(10) unsigned NOT NULL,
    evtID integer unsigned NOT NULL,
    sfFileName varchar(255) NOT NULL,
    sfFileCheckSum varchar(32) NOT NULL,
    sfFileSize varchar(255) NOT NULL,
    sfUploadedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    usrID integer unsigned NOT NULL,
 PRIMARY KEY(sfID),
 KEY (sbjID),
 KEY (evtID),
 KEY (sfFileName),
 KEY (sfFileName),
 KEY (sfUploadedAt),
 KEY (usrID),
 CONSTRAINT `fk_SubjectFile_evtID` FOREIGN KEY (evtID) REFERENCES Event (evtID),
 CONSTRAINT `fk_SubjectFile_sbjID` FOREIGN KEY (sbjID) REFERENCES Subject (sbjID),
 CONSTRAINT `fk_SubjectFile_usrID` FOREIGN KEY (usrID) REFERENCES User (usrID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE
    ALGORITHM=UNDEFINED
    DEFINER=`redidropper`@`localhost`
    VIEW `subject_file_view`
AS
SELECT
    sbjID, sbjRedcapID, evtID, evtRedcapArm, evtRedcapEvent, COUNT(sfFileName) AS totalEventFiles
FROM
    Subject
    JOIN SubjectFile USING (sbjID)
    JOIN Event USING (evtID)
GROUP BY
    sbjRedcapID, evtID
ORDER BY
    sbjRedcapID, evtRedcapArm, evtRedcapEvent
;


-- user agent parsing http://werkzeug.pocoo.org/docs/0.10/utils/
CREATE TABLE UserAgent (
    uaID integer unsigned NOT NULL AUTO_INCREMENT,
    uaUserAgent varchar(32768) NOT NULL DEFAULT '',
    uaHash varchar(32) NOT NULL,
    uaPlatform varchar(255) NOT NULL,
    uaBrowser varchar(255) NOT NULL,
    uaVersion varchar(255) NOT NULL,
    uaLanguage varchar(255) NOT NULL,
 PRIMARY KEY (uaID),
 UNIQUE KEY (uaHash),
 KEY uaPlatform (uaPlatform),
 KEY (uaBrowser, uaVersion),
 KEY (uaLanguage)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

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

CREATE TABLE LogType (
    logtID integer unsigned NOT NULL AUTO_INCREMENT,
    logtType varchar(255) NOT NULL,
    logtDescription text NOT NULL,
 PRIMARY KEY (logtID),
 UNIQUE KEY (logtType)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE Log (
    logID integer unsigned NOT NULL AUTO_INCREMENT,
    logtID integer unsigned NOT NULL,
    logIP varchar(15) NOT NULL DEFAULT '',
    webID integer unsigned NOT NULL,
    logDateTime datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    logDetails text NOT NULL,
 PRIMARY KEY (logID),
 KEY (logtID),
 KEY (logIP),
 KEY (webID),
 KEY (logDateTime),
 CONSTRAINT `fk_Log_logtID` FOREIGN KEY (logtID) REFERENCES LogType (logtID),
 CONSTRAINT `fk_Event_webID` FOREIGN KEY (webID) REFERENCES WebSession (webID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;


SHOW TABLES;
SELECT * FROM Version;
