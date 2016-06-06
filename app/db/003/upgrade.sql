-- ensure there will be no duplicates user / user role pairs
ALTER TABLE UserRole
ADD CONSTRAINT uc_UserIDRoleID UNIQUE (usrID, rolID);

-- add the logtype for the edit_user api call
INSERT INTO LogType
(logtType, logtDescription)
VALUES
('account_updated','');
