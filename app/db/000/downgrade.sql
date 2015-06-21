
DROP DATABASE IF EXISTS ctsi_dropper_s;
REVOKE ALL PRIVILEGES ON ctsi_dropper_s.* FROM 'ctsi_dropper_s'@'localhost';
DROP USER 'ctsi_dropper_s'@'localhost';
FLUSH PRIVILEGES;
