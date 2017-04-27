-- temporarily remove foreign keys to remove unique index
ALTER TABLE UserRole DROP FOREIGN KEY fk_User_usrID;
ALTER TABLE UserRole DROP FOREIGN KEY fk_UserRole_rolID;

-- remove unique index from UserRole
ALTER TABLE UserRole DROP INDEX uc_UserIDRoleID;

-- reapply the foreign key constraints
ALTER TABLE UserRole ADD CONSTRAINT fk_User_usrID FOREIGN KEY (usrID) REFERENCES User (usrID) ON DELETE CASCADE;
ALTER TABLE UserRole ADD CONSTRAINT fk_UserRole_rolID FOREIGN KEY (rolID) REFERENCES Role (rolID) ON DELETE CASCADE;

-- remove the log type for the edit user api call
DELETE FROM LogType
WHERE logtType='account_updated';
