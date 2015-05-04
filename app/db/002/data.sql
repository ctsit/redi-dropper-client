
USE RediDropper;

SET @end = CONCAT(CURDATE() + interval 6 month, ' 23:59:59');
SET @end2 = CONCAT(CURDATE() - interval 1 month, ' 23:59:59');


INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt, usrAccessExpiresAt, usrIsActive, usrEmailConfirmedAt)
VALUES
    ('admin@example.com', 'Admin', 'Adminsky', NOW(), @end, 1, NOW());
INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt, usrAccessExpiresAt, usrIsActive)
VALUES
    ('admin_blocked@example.com', 'Admin', 'Adminsky', NOW(), @end, 0),
    ('admin_expired@example.com', 'Admin', 'Adminsky', NOW(), @end2, 1),
    ('technician@example.com', 'Technician', 'Țărnă', NOW(), @end, 1),
    ('researcher_one@example.com', 'Researcher 1', 'de Méziriac', NOW(), @end, 1),
    ('researcher_two@example.com', 'Researcher 2', 'Bauchspeicheldrüsenkrebs',NOW(), @end, 1)
;



INSERT INTO Role (rolName, rolDescription)
VALUES
    ('admin', 'Can add/edit users, roles, log events; upload/delete images'),
    ('technician', 'Can upload/delete images'),
    ('researcher_one', 'Can upload/download images'),
    ('researcher_two', 'Can upload/download images')
;



INSERT INTO UserRole (usrID, rolID, urAddedAt)
      SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'admin@example.com' AND rolName = 'admin'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'admin_blocked@example.com' AND rolName = 'admin'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'admin_expired@example.com' AND rolName = 'admin'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'admin@example.com' AND rolName = 'technician'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'admin@example.com' AND rolName = 'researcher_one'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'admin@example.com' AND rolName = 'researcher_two'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'technician@example.com' AND rolName = 'technician'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'researcher_one@example.com' AND rolName = 'researcher_one'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'researcher_two@example.com' AND rolName = 'researcher_two'
;

-- Subjects
INSERT INTO Subject (sbjRedcapID, sbjAddedAt)
VALUES
    ('001', NOW()),
    ('002', NOW()),
    ('003', NOW()),
    ('004', NOW()),
    ('005', NOW())
;


-- REDCap event
INSERT INTO Event (evtRedcapArm, evtRedcapEvent, evtAddedAt)
        SELECT 'Arm 1', 'Event 01', NOW()
UNION   SELECT 'Arm 1', 'Event 02', NOW()
UNION   SELECT 'Arm 1', 'Event 03', NOW()
UNION   SELECT 'Arm 1', 'Event 04', NOW()
UNION   SELECT 'Arm 1', 'Event 05', NOW()
UNION   SELECT 'Arm 1', 'Event 06', NOW()
UNION   SELECT 'Arm 1', 'Event 07', NOW()
UNION   SELECT 'Arm 1', 'Event 08', NOW()
UNION   SELECT 'Arm 1', 'Event 09', NOW()
UNION   SELECT 'Arm 1', 'Event 10', NOW()
UNION   SELECT 'Arm 1', 'Event 11', NOW()
UNION   SELECT 'Arm 1', 'Event 12', NOW()
UNION   SELECT 'Arm 1', 'Event 13', NOW()
UNION   SELECT 'Arm 1', 'Event 14', NOW()
UNION   SELECT 'Arm 1', 'Event 15', NOW()
UNION   SELECT 'Arm 1', 'Event 16', NOW()
UNION   SELECT 'Arm 1', 'Event 17', NOW()
UNION   SELECT 'Arm 1', 'Event 18', NOW()
UNION   SELECT 'Arm 1', 'Event 19', NOW()
UNION   SELECT 'Arm 1', 'Event 20', NOW()
;


-- Subject Files
INSERT INTO SubjectFile (sbjID, evtID, sfFileName, sfFileCheckSum, sfFileSize, sfUploadedAt, usrID)
        SELECT 1, 1, 'file.png',  md5('a'), '1 MB', NOW(), 1
UNION   SELECT 1, 1, 'file2.png', md5('b'), '1 MB', NOW(), 1
UNION   SELECT 1, 1, 'file3.png', md5('c'), '1 MB', NOW(), 1
UNION   SELECT 1, 2, 'file4.png', md5('d'), '1 MB', NOW(), 1
UNION   SELECT 1, 2, 'file5.png', md5('e'), '1 MB', NOW(), 1
UNION   SELECT 1, 2, 'file6.png', md5('f'), '1 MB', NOW(), 1
UNION   SELECT 1, 3, 'file7.png', md5('g'), '1 MB', NOW(), 1
UNION   SELECT 1, 3, 'file8.png', md5('h'), '1 MB', NOW(), 1
UNION   SELECT 1, 4, 'file9.png', md5('i'), '1 MB', NOW(), 1
UNION   SELECT 1, 5, 'fileA.png', md5('j'), '1 MB', NOW(), 1
UNION   SELECT 1, 6, 'fileB.png', md5('k'), '1 MB', NOW(), 1
UNION   SELECT 1, 7, 'fileC.png', md5('l'), '1 MB', NOW(), 1
UNION   SELECT 1, 7, 'fileD.png', md5('m'), '1 MB', NOW(), 1
UNION   SELECT 1, 8, 'fileE.png', md5('n'), '1 MB', NOW(), 1
UNION   SELECT 1, 8, 'fileF.png', md5('o'), '1 MB', NOW(), 1
UNION   SELECT 1, 9, 'fileG.png', md5('p'), '1 MB', NOW(), 1
UNION   SELECT 1, 9, 'fileH.png', md5('q'), '1 MB', NOW(), 1

UNION   SELECT 2, 1, 'file.png',  md5('a'), '1 MB', NOW(), 1
UNION   SELECT 2, 2, 'file2.png', md5('b'), '1 MB', NOW(), 1
UNION   SELECT 2, 2, 'file3.png', md5('c'), '1 MB', NOW(), 1
UNION   SELECT 2, 2, 'file4.png', md5('d'), '1 MB', NOW(), 1
UNION   SELECT 2, 2, 'file5.png', md5('e'), '1 MB', NOW(), 1
UNION   SELECT 2, 2, 'file6.png', md5('f'), '1 MB', NOW(), 1
UNION   SELECT 2, 3, 'file7.png', md5('g'), '1 MB', NOW(), 1
UNION   SELECT 2, 3, 'file8.png', md5('h'), '1 MB', NOW(), 1
UNION   SELECT 2, 4, 'file9.png', md5('i'), '1 MB', NOW(), 1
UNION   SELECT 2, 5, 'fileA.png', md5('j'), '1 MB', NOW(), 2
UNION   SELECT 2, 5, 'fileB.png', md5('k'), '1 MB', NOW(), 2
UNION   SELECT 2, 5, 'fileC.png', md5('l'), '1 MB', NOW(), 2
UNION   SELECT 2, 5, 'fileD.png', md5('m'), '1 MB', NOW(), 2
UNION   SELECT 2, 5, 'fileE.png', md5('n'), '1 MB', NOW(), 2
UNION   SELECT 2, 6, 'fileF.png', md5('o'), '1 MB', NOW(), 2
UNION   SELECT 2, 7, 'fileG.png', md5('p'), '1 MB', NOW(), 2
UNION   SELECT 2, 7, 'fileH.png', md5('q'), '1 MB', NOW(), 2

UNION   SELECT 3, 1, 'file.png',  md5('a'), '1 MB', NOW(), 1
UNION   SELECT 3, 2, 'file2.png', md5('b'), '1 MB', NOW(), 1
UNION   SELECT 3, 2, 'file3.png', md5('c'), '1 MB', NOW(), 1
UNION   SELECT 3, 2, 'file4.png', md5('d'), '1 MB', NOW(), 1
UNION   SELECT 3, 2, 'file5.png', md5('e'), '1 MB', NOW(), 1
UNION   SELECT 3, 2, 'file6.png', md5('f'), '1 MB', NOW(), 1
UNION   SELECT 3, 3, 'file7.png', md5('g'), '1 MB', NOW(), 1
UNION   SELECT 3, 3, 'file8.png', md5('h'), '1 MB', NOW(), 1
UNION   SELECT 3, 3, 'file9.png', md5('i'), '1 MB', NOW(), 1
UNION   SELECT 3, 3, 'fileA.png', md5('j'), '1 MB', NOW(), 2
UNION   SELECT 3, 3, 'fileB.png', md5('k'), '1 MB', NOW(), 2
UNION   SELECT 3, 3, 'fileC.png', md5('l'), '1 MB', NOW(), 2
UNION   SELECT 3, 4, 'fileD.png', md5('m'), '1 MB', NOW(), 2
UNION   SELECT 3, 4, 'fileE.png', md5('n'), '1 MB', NOW(), 2
UNION   SELECT 3, 5, 'fileF.png', md5('o'), '1 MB', NOW(), 2
UNION   SELECT 3, 6, 'fileG.png', md5('p'), '1 MB', NOW(), 2
UNION   SELECT 3, 7, 'fileH.png', md5('q'), '1 MB', NOW(), 2

UNION   SELECT 4, 1, 'file.png',  md5('a'), '1 MB', NOW(), 1
UNION   SELECT 4, 1, 'file2.png', md5('b'), '1 MB', NOW(), 1
UNION   SELECT 4, 2, 'file3.png', md5('c'), '1 MB', NOW(), 1
UNION   SELECT 4, 3, 'file4.png', md5('d'), '1 MB', NOW(), 1
UNION   SELECT 4, 3, 'file5.png', md5('e'), '1 MB', NOW(), 1
UNION   SELECT 4, 3, 'file6.png', md5('f'), '1 MB', NOW(), 1
UNION   SELECT 4, 4, 'file7.png', md5('g'), '1 MB', NOW(), 1
UNION   SELECT 4, 5, 'file8.png', md5('h'), '1 MB', NOW(), 1
UNION   SELECT 4, 6, 'file9.png', md5('i'), '1 MB', NOW(), 1
UNION   SELECT 4, 7, 'fileA.png', md5('j'), '1 MB', NOW(), 2
UNION   SELECT 4, 8, 'fileB.png', md5('k'), '1 MB', NOW(), 2
UNION   SELECT 4, 3, 'fileC.png', md5('l'), '1 MB', NOW(), 2
UNION   SELECT 4, 9, 'fileD.png', md5('m'), '1 MB', NOW(), 2
UNION   SELECT 4,10, 'fileE.png', md5('n'), '1 MB', NOW(), 2
UNION   SELECT 4,11, 'fileF.png', md5('o'), '1 MB', NOW(), 2
UNION   SELECT 4,12, 'fileG.png', md5('p'), '1 MB', NOW(), 2
UNION   SELECT 4,13, 'fileH.png', md5('q'), '1 MB', NOW(), 2
;


-- Logging

-- add event types
INSERT INTO LogType
    (logtType, logtDescription)
VALUES
    ('account_created', ''),
    ('login', ''),
    ('logout', ''),
    ('login_error', ''),
    ('file_uploaded', ''),
    ('file_downloaded', '')
;

INSERT INTO UserAgent(uaUserAgent, uaHash, uaPlatform, uaBrowser, uaVersion, uaLanguage)
    VALUES ('Firefox 123', md5('Firefox 123'), 'OS X', 'Firefox', '123', 'EN')
;

INSERT INTO WebSession (webSessID, usrID, webIP, webDateTime, uaID)
VALUES
    (md5('ha'), 1, '192.168.1.1', NOW(), 1),
    (md5('ha2'), 1, '172.27.1.100', NOW(), 1)
;


INSERT INTO Log (logtID, logIP, webID, logDateTime, logDetails)
      SELECT logtID, '1.2.3.4', 1, NOW(), 'no details' FROM LogType WHERE logtType = 'account_created'
UNION SELECT logtID, '1.2.3.4', 1, NOW(), 'no details' FROM LogType WHERE logtType = 'login'
UNION SELECT logtID, '1.2.3.4', 1, NOW(), 'no details' FROM LogType WHERE logtType = 'logout'
UNION SELECT logtID, '1.2.3.4', 1, NOW(), 'no details' FROM LogType WHERE logtType = 'login_error'
UNION SELECT logtID, '1.2.3.4', 1, NOW(), 'no details' FROM LogType WHERE logtType = 'file_uploaded'
UNION SELECT logtID, '1.2.3.4', 1, NOW(), 'no details' FROM LogType WHERE logtType = 'file_downloaded'
;
