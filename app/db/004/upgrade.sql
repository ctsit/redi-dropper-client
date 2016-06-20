--add the deleter permission
INSERT INTO Role (rolName, rolDescription) VALUES ('deleter', 'Can delete files');

--add the file deleted log type
INSERT INTO LogType
(logtType, logtDescription)
VALUES
('file_deleted','');
