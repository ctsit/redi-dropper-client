
-- Create the user and grant privileges
CREATE USER 'ctsi_dropper_s'@'localhost' IDENTIFIED BY 'insecurepassword';
GRANT
    INSERT, SELECT, UPDATE, DELETE
    , SHOW VIEW
ON
    ctsi_dropper_s.*
TO
    'ctsi_dropper_s'@'localhost';

FLUSH PRIVILEGES;


CREATE DATABASE ctsi_dropper_s;
