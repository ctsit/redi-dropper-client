
-- USE ctsi_dropper_s;

SET @end = CONCAT(CURDATE() + interval 6 month, ' 23:59:59');
SET @end2 = CONCAT(CURDATE() - interval 1 month, ' 23:59:59');


-- Note: there is no value inserted in the usrPasswordHash
INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt, usrAccessExpiresAt, usrIsActive, usrEmailConfirmedAt)
VALUES
    ('asura@ufl.edu',           'Andrei',       'Şérenfaü',                     NOW(), @end, 1, NOW()),
    ('kshanson@ufl.edu',        'Kevin',        'Hanson',                       NOW(), @end, 1, NOW()),
    ('cpb@ufl.edu',             'Christopher',  'Barnes',                       NOW(), @end2, 1, NOW()),
    ('pbc@ufl.edu',             'Philip',       'Chase',                        NOW(), @end, 0, NOW()),
    ('keyes@ufl.edu',           'Roy',          'Keyes',                        NOW(), @end, 0, NOW()),
    ('taeber@ufl.edu',          'Taeber',       'Rapczak',                      NOW(), @end, 0, NOW())
;

INSERT INTO Role (rolName, rolDescription)
VALUES
    ('admin', 'Can add/edit users, roles, log events; upload/delete images'),
    ('technician', 'Can upload/delete images'),
    ('researcher_one', 'Can upload/download images'),
    ('researcher_two', 'Can upload/download images')
;

INSERT INTO UserRole (usrID, rolID, urAddedAt)
      SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'asura@ufl.edu' AND rolName = 'admin'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'kshanson@ufl.edu' AND rolName = 'admin'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'kshanson@ufl.edu' AND rolName = 'technician'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'kshanson@ufl.edu' AND rolName = 'researcher_one'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'kshanson@ufl.edu' AND rolName = 'researcher_two'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'cpb@ufl.edu' AND rolName = 'technician'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'pbc@ufl.edu' AND rolName = 'technician'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'keyes@ufl.edu' AND rolName = 'technician'
UNION SELECT usrID, rolID, NOW() FROM User, Role WHERE usrEmail = 'taeber@ufl.edu' AND rolName = 'technician'
;


-- Subject Files
-- INSERT INTO SubjectFile (sbjID, evtID, sfFileName, sfFileCheckSum, sfFileSize, sfUploadedAt, usrID)
--        SELECT 1, 1, 'test_file.png',  md5('a'), '123', NOW(), 1
-- UNION   SELECT 1, 1, 'test_file2.png', md5('b'), '456', NOW(), 1;

-- Logging

-- add event types
INSERT INTO LogType
    (logtType, logtDescription)
VALUES
    ('account_created', ''),
    ('account_updated',''),
    ('login', ''),
    ('logout', ''),
    ('login_error', ''),
    ('file_uploaded', ''),
    ('file_downloaded', ''),
    ('account_modified', ''),
    ('redcap_subjects_impported', ''),
    ('redcap_events_imported', '')
;

INSERT INTO UserAgent(uaUserAgent, uaHash, uaPlatform, uaBrowser, uaVersion, uaLanguage)
    VALUES ('Firefox 123', md5('Firefox 123'), 'OS X', 'Firefox', '123', 'EN')
;

-- INSERT INTO WebSession (webSessID, usrID, webIP, webDateTime, uaID)
-- VALUES
--     (uuid(), 1, '192.168.1.1', NOW(), 1),
--     (uuid(), 1, '172.27.1.100', NOW(), 1)
-- ;


-- INSERT INTO Log (logtID, webID, logDateTime, logDetails)
--       SELECT logtID, 1, NOW(), 'no details' FROM LogType WHERE logtType = 'account_created'
-- UNION SELECT logtID, 1, NOW(), 'no details' FROM LogType WHERE logtType = 'account_updated'
-- UNION SELECT logtID, 1, NOW(), 'no details' FROM LogType WHERE logtType = 'login'
-- UNION SELECT logtID, 1, NOW(), 'no details' FROM LogType WHERE logtType = 'logout'
-- UNION SELECT logtID, 1, NOW(), 'no details' FROM LogType WHERE logtType = 'login_error'
-- UNION SELECT logtID, 1, NOW(), 'no details' FROM LogType WHERE logtType = 'file_uploaded'
-- UNION SELECT logtID, 1, NOW(), 'no details' FROM LogType WHERE logtType = 'file_downloaded'
-- ;
