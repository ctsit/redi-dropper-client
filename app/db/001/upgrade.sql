
USE ctsi_dropper_s;

-- Store database modification log
CREATE TABLE Version (
   verID varchar(255) NOT NULL DEFAULT '',
   verStamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   verInfo text NOT NULL,
  PRIMARY KEY (verID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Version (verID, verInfo)
   VALUES('001', 'New table: Version')
;


SHOW TABLES;
SELECT * FROM Version;
