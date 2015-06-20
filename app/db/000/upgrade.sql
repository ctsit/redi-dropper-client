
-- Create the user and grant privileges
CREATE USER 'redidropper'@'localhost' IDENTIFIED BY 'insecurepassword';
GRANT
    INSERT, SELECT, UPDATE, DELETE
    , SHOW VIEW
ON
    RediDropper.*
TO
    'redidropper'@'localhost';

FLUSH PRIVILEGES;


CREATE DATABASE RediDropper;

