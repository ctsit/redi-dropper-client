-- remove the deleter permission
DELETE FROM Roles
WHERE rolName='deleter'

-- remove the log type for the edit user api call
DELETE FROM LogType
WHERE logtType='file_deleted';
