
USE RediDropper;


INSERT INTO Role (rolName, rolDescription)
VALUES
    ('admin', 'Can edit users, roles, projects'),
    ('technician', 'Can upload/delete images'),
    ('researcher_one', 'Can upload/download images'),
    ('researcher_two', 'Can upload/download images')
;


INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt)
VALUES
    ('admin@example.com', 'Admin', 'Adminsky', NOW())
;

INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt)
VALUES
    ('technician@example.com', 'Technician', 'Țărnă', NOW())
;

INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt)
VALUES
    ('researcher_one@example.com', 'Researcher 1', 'de Méziriac', NOW())
;

INSERT INTO User (usrEmail, usrFirst, usrLast, usrAddedAt)
VALUES
    ('researcher_two@example.com', 'Researcher 2', 'Bauchspeicheldrüsenkrebs',NOW())
;


INSERT INTO Project (prjUrlHost, prjUrlPath, prjName, prjApiKey, prjAddedAt)
VALUES
    ('http://localhost:8081', '/redcap/redcap_v6.0.5/ProjectSetup/index.php?pid=34', 'ADRC TEST', 'FC25694A0BFD3602362992E12DC89DB3', NOW()),
    ('http://localhost:8998', '/redcap_v5.7.4/ProjectSetup/index.php?pid=12', 'PMP TEST', '121212', NOW())
;


INSERT INTO ProjectUserRole (prjID, usrID, rolID)
SELECT
    prjID, usrID, rolID
FROM
    Project, User, Role
WHERE
    prjName = 'ADRC TEST'
    AND usrEmail = 'admin@example.com'
    AND rolName = 'admin'
;

INSERT INTO ProjectUserRole (prjID, usrID, rolID)
SELECT
    prjID, usrID, rolID
FROM
    Project, User, Role
WHERE
    prjName = 'ADRC TEST'
    AND usrEmail = 'technician@example.com'
    AND rolName = 'technician'
;


INSERT INTO ProjectUserRole (prjID, usrID, rolID)
SELECT
    prjID, usrID, rolID
FROM
    Project, User, Role
WHERE
    prjName = 'ADRC TEST'
    AND usrEmail = 'researcher_one@example.com'
    AND rolName = 'researcher_one'
;

INSERT INTO ProjectUserRole (prjID, usrID, rolID)
SELECT
    prjID, usrID, rolID
FROM
    Project, User, Role
WHERE
    prjName = 'ADRC TEST'
    AND usrEmail = 'researcher_two@example.com'
    AND rolName = 'researcher_two'
;


INSERT INTO UserAuth (usrID, uathUsername, uathPassword)
SELECT
    usrID, 'admin', 'password'
FROM
    User
WHERE
    usrEmail = 'admin@example.com'
;

INSERT INTO UserAuth (usrID, uathUsername, uathPassword)
SELECT
    usrID, 'technician', 'password'
FROM
    User
WHERE
    usrEmail = 'technician@example.com'
;

-- second project
INSERT INTO ProjectUserRole (prjID, usrID, rolID)
SELECT
    prjID, usrID, rolID
FROM
    Project, User, Role
WHERE
    prjName = 'PMP TEST'
    AND usrEmail = 'admin@example.com'
    AND rolName = 'technician'
;
