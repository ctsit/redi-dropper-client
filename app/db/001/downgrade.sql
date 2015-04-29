
DROP DATABASE IF EXISTS RediDropper;
REVOKE ALL PRIVILEGES ON RediDropper.* FROM 'redidropper'@'localhost';
DROP USER 'redidropper'@'localhost';
FLUSH PRIVILEGES;
