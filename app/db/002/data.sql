
USE RediDropper;

SET @end = CONCAT(CURDATE() + interval 6 month, ' 23:59:59');

INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt, usrAccessExpiresAt)
VALUES
    ('admin@example.com', 'Admin', 'Adminsky', NOW(), @end),
    ('technician@example.com', 'Technician', 'Țărnă', NOW(), @end),
    ('researcher_one@example.com', 'Researcher 1', 'de Méziriac', NOW(), @end),
    ('researcher_two@example.com', 'Researcher 2', 'Bauchspeicheldrüsenkrebs',NOW(), @end)
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
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'admin@example.com' AND rolName = 'technician'
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


-- Subject Files
INSERT INTO SubjectFile (sbjID, sfEventNumber, sfFileName, sfFileCheckSum, sfUploadDate, usrID)
        SELECT 1, 1, 'file.png',  md5('a'), NOW(), 1
UNION   SELECT 1, 1, 'file2.png', md5('b'), NOW(), 1
UNION   SELECT 1, 1, 'file3.png', md5('c'), NOW(), 1
UNION   SELECT 1, 2, 'file4.png', md5('d'), NOW(), 1
UNION   SELECT 1, 2, 'file5.png', md5('e'), NOW(), 1
UNION   SELECT 1, 2, 'file6.png', md5('f'), NOW(), 1
UNION   SELECT 1, 3, 'file7.png', md5('g'), NOW(), 1
UNION   SELECT 1, 3, 'file8.png', md5('h'), NOW(), 1
UNION   SELECT 1, 4, 'file9.png', md5('i'), NOW(), 1
UNION   SELECT 1, 5, 'fileA.png', md5('j'), NOW(), 1
UNION   SELECT 1, 6, 'fileB.png', md5('k'), NOW(), 1
UNION   SELECT 1, 7, 'fileC.png', md5('l'), NOW(), 1
UNION   SELECT 1, 7, 'fileD.png', md5('m'), NOW(), 1
UNION   SELECT 1, 8, 'fileE.png', md5('n'), NOW(), 1
UNION   SELECT 1, 8, 'fileF.png', md5('o'), NOW(), 1
UNION   SELECT 1, 9, 'fileG.png', md5('p'), NOW(), 1
UNION   SELECT 1, 9, 'fileH.png', md5('q'), NOW(), 1

UNION   SELECT 2, 1, 'file.png',  md5('a'), NOW(), 1
UNION   SELECT 2, 2, 'file2.png', md5('b'), NOW(), 1
UNION   SELECT 2, 2, 'file3.png', md5('c'), NOW(), 1
UNION   SELECT 2, 2, 'file4.png', md5('d'), NOW(), 1
UNION   SELECT 2, 2, 'file5.png', md5('e'), NOW(), 1
UNION   SELECT 2, 2, 'file6.png', md5('f'), NOW(), 1
UNION   SELECT 2, 3, 'file7.png', md5('g'), NOW(), 1
UNION   SELECT 2, 3, 'file8.png', md5('h'), NOW(), 1
UNION   SELECT 2, 4, 'file9.png', md5('i'), NOW(), 1
UNION   SELECT 2, 5, 'fileA.png', md5('j'), NOW(), 2
UNION   SELECT 2, 5, 'fileB.png', md5('k'), NOW(), 2
UNION   SELECT 2, 5, 'fileC.png', md5('l'), NOW(), 2
UNION   SELECT 2, 5, 'fileD.png', md5('m'), NOW(), 2
UNION   SELECT 2, 5, 'fileE.png', md5('n'), NOW(), 2
UNION   SELECT 2, 6, 'fileF.png', md5('o'), NOW(), 2
UNION   SELECT 2, 7, 'fileG.png', md5('p'), NOW(), 2
UNION   SELECT 2, 7, 'fileH.png', md5('q'), NOW(), 2

UNION   SELECT 3, 1, 'file.png',  md5('a'), NOW(), 1
UNION   SELECT 3, 2, 'file2.png', md5('b'), NOW(), 1
UNION   SELECT 3, 2, 'file3.png', md5('c'), NOW(), 1
UNION   SELECT 3, 2, 'file4.png', md5('d'), NOW(), 1
UNION   SELECT 3, 2, 'file5.png', md5('e'), NOW(), 1
UNION   SELECT 3, 2, 'file6.png', md5('f'), NOW(), 1
UNION   SELECT 3, 3, 'file7.png', md5('g'), NOW(), 1
UNION   SELECT 3, 3, 'file8.png', md5('h'), NOW(), 1
UNION   SELECT 3, 3, 'file9.png', md5('i'), NOW(), 1
UNION   SELECT 3, 3, 'fileA.png', md5('j'), NOW(), 2
UNION   SELECT 3, 3, 'fileB.png', md5('k'), NOW(), 2
UNION   SELECT 3, 3, 'fileC.png', md5('l'), NOW(), 2
UNION   SELECT 3, 4, 'fileD.png', md5('m'), NOW(), 2
UNION   SELECT 3, 4, 'fileE.png', md5('n'), NOW(), 2
UNION   SELECT 3, 5, 'fileF.png', md5('o'), NOW(), 2
UNION   SELECT 3, 6, 'fileG.png', md5('p'), NOW(), 2
UNION   SELECT 3, 7, 'fileH.png', md5('q'), NOW(), 2

UNION   SELECT 4, 1, 'file.png',  md5('a'), NOW(), 1
UNION   SELECT 4, 1, 'file2.png', md5('b'), NOW(), 1
UNION   SELECT 4, 2, 'file3.png', md5('c'), NOW(), 1
UNION   SELECT 4, 3, 'file4.png', md5('d'), NOW(), 1
UNION   SELECT 4, 3, 'file5.png', md5('e'), NOW(), 1
UNION   SELECT 4, 3, 'file6.png', md5('f'), NOW(), 1
UNION   SELECT 4, 4, 'file7.png', md5('g'), NOW(), 1
UNION   SELECT 4, 5, 'file8.png', md5('h'), NOW(), 1
UNION   SELECT 4, 6, 'file9.png', md5('i'), NOW(), 1
UNION   SELECT 4, 7, 'fileA.png', md5('j'), NOW(), 2
UNION   SELECT 4, 8, 'fileB.png', md5('k'), NOW(), 2
UNION   SELECT 4, 3, 'fileC.png', md5('l'), NOW(), 2
UNION   SELECT 4, 9, 'fileD.png', md5('m'), NOW(), 2
UNION   SELECT 4,10, 'fileE.png', md5('n'), NOW(), 2
UNION   SELECT 4,11, 'fileF.png', md5('o'), NOW(), 2
UNION   SELECT 4,12, 'fileG.png', md5('p'), NOW(), 2
UNION   SELECT 4,13, 'fileH.png', md5('q'), NOW(), 2
;


-- Logging

-- add event types
INSERT INTO EventType
    (evttType, evttDescription)
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


INSERT INTO Event (evttID, evtIP, webID, evtDateTime)
      SELECT evttID, '1.2.3.4', 1, NOW() FROM EventType WHERE evttType = 'account_created'
UNION SELECT evttID, '1.2.3.4', 1, NOW() FROM EventType WHERE evttType = 'login'
UNION SELECT evttID, '1.2.3.4', 1, NOW() FROM EventType WHERE evttType = 'logout'
UNION SELECT evttID, '1.2.3.4', 1, NOW() FROM EventType WHERE evttType = 'login_error'
UNION SELECT evttID, '1.2.3.4', 1, NOW() FROM EventType WHERE evttType = 'file_uploaded'
UNION SELECT evttID, '1.2.3.4', 1, NOW() FROM EventType WHERE evttType = 'file_downloaded'
;
