
USE RediDropper;
DROP TABLE Version;

REVOKE ALL PRIVILEGES ON RediDropper.* FROM 'redidropper'@'localhost';
DROP USER 'redidropper'@'localhost';
DROP DATABASE RediDropper;
