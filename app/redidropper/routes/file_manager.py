"""
Goal: Implement code specific to file handling on server side

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>

@TODO: read
    https://www.owasp.org/index.php/XSS_%28Cross_Site_Scripting%29_Prevention_Cheat_Sheet
    https://pypi.python.org/pypi/bleach
"""

import os
from datetime import datetime

from flask import request
from flask import session
from flask_login import current_user
from redidropper.models.log_entity import LogEntity
from werkzeug import secure_filename

from redidropper import utils
from redidropper.main import app, db
from redidropper.models.subject_entity import SubjectEntity
from redidropper.models.subject_file_entity import SubjectFileEntity

logger = app.logger


class FileChunk(object):

    """ Properties storage for a file chunk """
    @classmethod
    def init_from_request(cls):
        """
        Copy the request data about the file chunk into an object we can
        pass around functions that need the data
        """
        self = FileChunk()
        # @TODO: !!! add size checks for user input
        self.number = int(request.form['resumableChunkNumber'])
        self.size = int(request.form['resumableChunkSize'])
        self.total_size = int(request.form['resumableTotalSize'])
        self.uniqueid = request.form['resumableIdentifier']
        self.file_name = secure_filename(request.form['resumableFilename'])
        self.file_type = request.form['resumableFileType']
        self.afile = request.files['file']
        self.total_parts = int(request.form['resumableTotalChunks'])
        self.redcap_id = request.form['subject_id']  # @TODO: rename
        self.event_id = int(request.form['event_id'])
        return self

    def __repr__(self):
        """ Implement an unambiguous representation """
        return "FileChunk <{0.number} out of {0.total_parts} for file:" \
               "{0.file_name} ({0.size} out of {0.total_size} bytes)>" \
               .format(self)


def save_file_metadata(fchunk):
    """
    Insert a row in SubjectFile table to preserve file details.
    Called from api.py#api_upload() -> #save_uploaded_file() -> #merge_files()

    @return SubjectFileEntity
    """
    added_date = datetime.today()
    subject = SubjectEntity.get_by_redcap_id(fchunk.redcap_id)

    subject_file = SubjectFileEntity.create(
        subject_id=subject.id,
        event_id=fchunk.event_id,
        file_name=fchunk.file_name,
        file_check_sum='pending',
        file_size=fchunk.total_size,
        file_type=fchunk.file_type,
        uploaded_at=added_date,
        user_id=current_user.id)
    logger.debug("Saved metadata to the db: ".format(subject_file))
    return subject_file


def get_chunk_path(file_name, chunk_number):
    """ Helper for building path to temp dir """
    name = "{}.part{}".format(file_name, chunk_number)
    return os.path.join(app.config['REDIDROPPER_UPLOAD_TEMP_DIR'], name)


def save_uploaded_file():
    """ Receives files on the server side """
    fchunk = FileChunk.init_from_request()
    logger.info("User uploaded chunk: {}".format(fchunk))
    file_name = fchunk.file_name

    if not fchunk.afile:
        err = utils.pack_error("No file specified.")
        logger.error(err)
        return err

    chunk_path = get_chunk_path(file_name, fchunk.number)

    try:
        # For every request recived we store the chunk to a temp folder
        fchunk.afile.save(chunk_path)
    except Exception as exc:
        logger.error("Problem saving: {} due: {}".format(fchunk, exc))
        return utils.pack_error("Unable to save file chunk: {}"
                                .format(fchunk.number))

    # When all chunks are recived we merge them
    if not all_chunks_received(fchunk):
        return utils.jsonify_success('Request completed successfully.')

    # When all chunks are received we merge them
    subject_file = merge_files(fchunk)

    """
    get the path of the file or directory
    add the directory to a queue
    """

    if subject_file is not None:
        prefix = app.config['REDIDROPPER_UPLOAD_SAVED_DIR']
        file_path = subject_file.get_full_path(prefix)
        delete_temp_files(fchunk)
        hash_matches = verify_file_integrity(fchunk)

        if hash_matches:
            LogEntity.file_uploaded(session['uuid'],
                                    file_path)
            return utils.jsonify_success('File {} uploaded successfully.'
                                         .format(file_name))
        else:
            logger.error("md5 sum does not match for: {}".format(fchunk))
            LogEntity.file_uploaded(session['uuid'],
                                    'Checksum mismatch for file: {}'
                                    .format(file_path))
            return utils.jsonify_error('Checksum mismatch for file: {}'
                                       .format(file_name))
    else:
        LogEntity.file_uploaded(session['uuid'],
                                'Unable to merge chunks for file: {}'
                                .format(file_path))
        return utils.jsonify_error('Unable to merge chunks for file: {}'
                                   .format(file_name))


def all_chunks_received(fchunk):
    """ Return True when all file pieces are received """
    done = False
    file_name = fchunk.file_name

    for i in range(1, fchunk.total_parts + 1):
        chunk_path = get_chunk_path(file_name, i)

        if os.path.isfile(chunk_path):
            if i == fchunk.total_parts:
                logger.debug("Verified all {} chunks received for {}."
                             .format(fchunk.total_parts, file_name))
                done = True
        else:
            break
    return done


def verify_file_integrity(fchunk):
    """
    @TODO: implement
    """
    logger.debug("Verify md5sum...{}".format(fchunk))
    return True


def delete_temp_files(fchunk):
    """ Delete file chunks after all received and merged """
    file_name = fchunk.file_name
    logger.debug("Removing {} file chunks for: {}"
                 .format(fchunk.total_parts, file_name))

    for i in range(1, fchunk.total_parts + 1):
        chunk_path = get_chunk_path(file_name, i)
        os.remove(chunk_path)


def merge_files(fchunk):
    """ Reconstruct the original file from chunks

    :rtype SubjectFileEntity or None if merging fails
    :return the object representing the file metadata
    """
    subject_file = save_file_metadata(fchunk)
    prefix = app.config['REDIDROPPER_UPLOAD_SAVED_DIR']
    file_path = subject_file.get_full_path(prefix)
    file_name = fchunk.file_name
    logger.debug("Saving file: {} consisting of {} chunks"
                 " in the destination folder: {}."
                 .format(file_name, fchunk.total_parts, prefix))

    try:
        f = open(file_path, "w")

        for i in range(1, fchunk.total_parts + 1):
            chunk_path = get_chunk_path(file_name, i)
            tempfile = open(chunk_path, "r")
            f.write(tempfile.read())
        # log_manager.log_file_upload(subject_file)
    except Exception as exc:
        subject_file = None
        logger.error("There was an issue in merge_files(): {}".format(exc))

    return subject_file

def delete_file(subject_file_id):
    """deletes a particular file

    :rtype tuple
    :return (subject_file_id, deleted_file_path)
    """

    file_entity = SubjectFileEntity.query.filter_by(id=subject_file_id).one()
    file_path = file_entity.get_full_path(app.config['REDIDROPPER_UPLOAD_SAVED_DIR'])
    os.remove(file_path)
    file_entity.delete()
    db.session.commit()
    return (subject_file_id, file_path)

def update_filetype(subject_file_id, subject_file_type):
    """ Updates the type field of the file """
    file_entity = SubjectFileEntity.query.filter_by(id=subject_file_id).one()
    file_entity.update(file_type=subject_file_type)
    db.session.commit()
    return (subject_file_id, subject_file_type)
