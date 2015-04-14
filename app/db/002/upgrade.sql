
USE RediDropper;

INSERT INTO Version (verID, verInfo)
    VALUES('002', 'Create tables: User, UserAuth, Role, Project, ProjectUserRole')
;


-- http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html

-- Store user's personal info
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
 PRIMARY KEY (usrID),
 UNIQUE KEY (usrEmail),
 KEY (usrFirst, usrLast),
 KEY (usrAddedAt),
 KEY (usrModifiedAt),
 KEY (usrEmailConfirmedAt)
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

-- Store project name, id, token (assumes only one token per project)
CREATE TABLE Project (
    prjID smallint unsigned NOT NULL AUTO_INCREMENT,
    prjName varchar(255) NOT NULL,
    prjUrlHost varchar(255) NOT NULL,
    prjUrlPath varchar(255) NOT NULL,
    prjApiKey varchar(255) NOT NULL DEFAULT '',
    prjAddedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    prjModifiedAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (prjID),
 UNIQUE KEY (prjUrlHost, prjUrlPath),
 KEY (prjName),
 KEY (prjAddedAt),
 KEY (prjModifiedAt)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

-- Store user roles mapping
CREATE TABLE ProjectUserRole (
    purID integer unsigned NOT NULL AUTO_INCREMENT,
    prjID smallint unsigned NOT NULL,
    usrID integer unsigned NOT NULL,
    rolID smallint unsigned NOT NULL,
 PRIMARY KEY (purID),
 UNIQUE KEY(prjID, usrID),
 CONSTRAINT `fk_ProjectUserRole_prjID` FOREIGN KEY (prjID) REFERENCES Project (prjID) ON DELETE CASCADE,
 CONSTRAINT `fk_ProjectUserRole_usrID` FOREIGN KEY (usrID) REFERENCES User (usrID) ON DELETE CASCADE,
 CONSTRAINT `fk_ProjectUserRole_rolID` FOREIGN KEY (rolID) REFERENCES Role (rolID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE UserAuth (
    uathID integer unsigned NOT NULL AUTO_INCREMENT,
    usrID integer unsigned NOT NULL,
    uathUsername varchar(255) NOT NULL,
    uathSalt varchar(255) NOT NULL,
    uathPassword varchar(255) NOT NULL,
    uathPasswordResetToken varchar(255) NOT NULL DEFAULT '',
    uathEmailConfirmationToken varchar(255) NOT NULL DEFAULT '',
    uathModifiedAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (uathID),
 UNIQUE KEY (usrID),
 UNIQUE KEY (uathUsername),
 CONSTRAINT `fk_UserAuth_usrID` FOREIGN KEY (usrID) REFERENCES User (usrID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE
    ALGORITHM=UNDEFINED
    DEFINER=`redidropper`@`localhost`
    VIEW `ProjectUserRoleView`
AS
SELECT
    prjID, prjName, usrID, usrEmail, rolID, rolName, uathID, uathUsername, uathPassword
FROM
    User
    JOIN ProjectUserRole USING (usrID)
    JOIN Project USING (prjID)
    JOIN Role USING (rolID)
    LEFT JOIN UserAuth USING(usrID)
WHERE
    usrIsActive
;


CREATE TABLE Subject (
    sbjID int(10) unsigned NOT NULL AUTO_INCREMENT,
    prjID smallint unsigned NOT NULL,
    sbjRedcapID varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    sbjAddedAt datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
 PRIMARY KEY (sbjID),
 UNIQUE KEY(prjID, sbjRedcapID),
 KEY (sbjRedcapID),
 KEY (sbjAddedAt),
 CONSTRAINT `fk_Subject_prjID` FOREIGN KEY (prjID) REFERENCES Project (prjID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;


CREATE TABLE SubjectFile (
    sfID int(10) unsigned NOT NULL AUTO_INCREMENT,
    sbjID int(10) unsigned NOT NULL,
    sfEventNumber smallint unsigned NOT NULL,
    sfFileName varchar(255) NOT NULL,
    sfFileCheckSum varchar(32) NOT NULL,
    sfUploadDate date NOT NULL,
    usrID integer unsigned NOT NULL,
 PRIMARY KEY(sfID),
 UNIQUE KEY (sbjID, sfEventNumber, sfFileName),
 KEY (sfFileName),
 KEY (sfUploadDate),
 KEY (usrID),
 CONSTRAINT `fk_SubjectFile_usrID` FOREIGN KEY (usrID) REFERENCES User (usrID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;


-- user agent parsing http://werkzeug.pocoo.org/docs/0.10/utils/
CREATE TABLE UserAgent (
    uaID int(10) unsigned NOT NULL AUTO_INCREMENT,
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
    uaID int(10) unsigned DEFAULT NULL,
 PRIMARY KEY (webID),
 KEY (usrID),
 KEY (webDateTime),
 KEY (uaID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE EventType (
    evttID integer unsigned NOT NULL AUTO_INCREMENT,
    evttType varchar(255) NOT NULL,
    evttDescription text NOT NULL,
 PRIMARY KEY (evttID),
 UNIQUE KEY (evttType)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE Event (
    evtID integer unsigned NOT NULL AUTO_INCREMENT,
    evttID integer unsigned NOT NULL,
    evtIP varchar(15) NOT NULL DEFAULT '',
    webID integer unsigned NOT NULL,
    evtDateTime datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    evtDetails text NOT NULL,
 PRIMARY KEY (evtID),
 KEY (evttID),
 KEY (evtIP),
 KEY (webID),
 KEY (evtDateTime),
 CONSTRAINT `fk_Event_webID` FOREIGN KEY (webID) REFERENCES WebSession (webID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;


SHOW TABLES;
SELECT * FROM Version;
