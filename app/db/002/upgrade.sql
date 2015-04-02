
USE RediDropper;

INSERT INTO Version (verID, verInfo)
    VALUES('002', 'Create tables: User, Role, Project, ProjectUserRole')
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
 UNIQUE KEY(prjID, usrID, rolID),
 CONSTRAINT `fk_Project_prjID` FOREIGN KEY (prjID) REFERENCES Project (prjID) ON DELETE CASCADE,
 CONSTRAINT `fk_User_usrID` FOREIGN KEY (usrID) REFERENCES User (usrID) ON DELETE CASCADE,
 CONSTRAINT `fk_Role_rolID` FOREIGN KEY (rolID) REFERENCES Role (rolID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
;

CREATE TABLE UserAuth (
    uathID integer unsigned NOT NULL AUTO_INCREMENT,
    usrID integer unsigned NOT NULL,
    uathUsername varchar(255) NOT NULL,
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
    VIEW UserProjectRoleView
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


SHOW TABLES;
SELECT * FROM Version;
