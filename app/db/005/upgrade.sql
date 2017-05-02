-- ensure there will be no duplicates user / user role pairs
ALTER TABLE SubjectFile
ADD sfFileType varchar(255) NOT NULL;
