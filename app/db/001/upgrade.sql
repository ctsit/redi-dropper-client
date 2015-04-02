
-- Create the user and grant privileges
CREATE USER 'redidropper'@'localhost' IDENTIFIED BY 'insecurepassword';
GRANT
    INSERT, SELECT, UPDATE, DELETE
    , SHOW VIEW
ON
    RediDropper.*
TO
    'redidropper'@'localhost';
FLUSH PRIVILEGES;


CREATE DATABASE RediDropper;
USE RediDropper;

-- Store database modification log
CREATE TABLE Version (
   verID varchar(255) NOT NULL DEFAULT '',
   verStamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   verInfo text NOT NULL,
  PRIMARY KEY (verID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Version (verID, verInfo)
   VALUES('001', 'Create initial database with versioning table')
;


SHOW TABLES;
SELECT * FROM Version;
