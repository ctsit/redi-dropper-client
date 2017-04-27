-- remove the deleter permission
DELETE FROM Role
WHERE rolName='deleter';

-- remove the log type for the edit user api call
DELETE FROM LogType
WHERE logtType='file_deleted';
