
-- USE ctsi_dropper_s;

-- shows active users but does not filter out the ones with usrAccessExpiresAt < NOW()
CREATE
    ALGORITHM=UNDEFINED
    DEFINER=`redidropper`@`localhost`
    VIEW `user_role_view`
AS
SELECT
    usrID, usrEmail, rolID, rolName, urAddedAt, usrAccessExpiresAt
FROM
    User
    JOIN UserRole USING (usrID)
    JOIN Role USING (rolID)
WHERE
    usrIsActive
;


CREATE
    ALGORITHM=UNDEFINED
    DEFINER=`redidropper`@`localhost`
    VIEW `subject_file_view`
AS
SELECT
    sbjID, sbjRedcapID, evtID, evtRedcapArm, evtRedcapEvent, COUNT(sfFileName) AS totalEventFiles
FROM
    Subject
    JOIN SubjectFile USING (sbjID)
    JOIN Event USING (evtID)
GROUP BY
    sbjRedcapID, evtID
ORDER BY
    sbjRedcapID, evtRedcapArm, evtRedcapEvent
;

