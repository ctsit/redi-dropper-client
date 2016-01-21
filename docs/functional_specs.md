# Functional Specification for the REDI-Dropper Application

## Authors

* Andrei Sura <asura@ufl.edu>
* Kevin Hanson <kshanson@ufl.edu>
* Philip Chase <pbc@ufl.edu>
* Christopher P. Barnes <cpb@ufl.edu>

## Overview

The RED-I Dropper application is a tool where by dynamic data is transferred
from multiple locations via a modern JavaScript framerwork over encrypted
channel to storage services for further processing. The application can be
customized to place datasets into processing environments that provide analysis
and quanitified data to aggregation points.


## Workflow and Use Cases

### Ella gets a MRI scan uploaded with RED-I Dropper for analysis.

Ella is a woman of latin heritage living in Miami, FL. She is a widow living
with her son-in-law and Daughter. She has undergone a neurocognitive assessment
with Dr. Miami and now she has been referred to the brain imaging specialists
at WeCare Hospital to have an MRI brain image performed. A technician conducts
the MRI image collection process. At the conclusion of which consortium staff
acquire the images and visit a website that is able to handle image uploads
potentially 3gb in size per study participant encounter. When the consortium
staff visits the website they utilize a Shibboleth account to
authenticate securely to the RED-I Dropper website.  Once logged on, the
consortium staff see a question asking them which subject goes with the MRI
scan. They see a list that shows the study participant’s ID.

Once the consortium staff verifies that the subject that was scanned is the
same as the one in the list they select the study participant. The staff is
prompted with a <b>file picker</b> where they are able to <b>select
all images</b> obtained from the MRI process at once and set them to upload.
Prior to an image upload the RED-I Dropper program <b>checks to see if a folder
exists</b> on the server for the subjectID and if it doesn't exist
then the <b>folder is created</b> the moment a file is uploaded. As the image
begins to upload, a <b>progress bar</b> displays for the upload process and once
completed they see a message saying “MRI scans for Ella have been uploaded,
thank you!”
The RED-I Dropper server then <b>prefixes the file names</b> with a <b>unique
identifier</b> in the format
“YYYYMMDD_HHMM_SiteID_SubjectID_5digtSequenceNumber” followed by the
<b>original file name</b>.

Example:
original filename: <b>xyz.jpg</b>
stored filename: 20120101_0123_SiteIDA_SubjectIDB_Sequence123_<b>xyz.jpg</b>
