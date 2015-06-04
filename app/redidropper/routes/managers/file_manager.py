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
from flask_login import current_user
from werkzeug import secure_filename

from redidropper import utils
from redidropper.main import app
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
        self.afile = request.files['file']
        self.total_parts = int(request.form['resumableTotalChunks'])
        self.subject_id = int(request.form['subject_id'])
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
    """
    # uploader = SubjectEntity.get_by_id(current_user.id)
    added_date = datetime.today()

    subject_file = SubjectFileEntity.create(
        subject_id=fchunk.subject_id,
        event_id=fchunk.event_id,
        file_name=fchunk.file_name,
        file_check_sum='pending',
        file_size=fchunk.total_size,
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

    if not utils.allowed_file(file_name):
        err = utils.pack_error("Invalid file type: {}."
                               "Allowed extensions: {}"
                               .format(file_name, utils.ALLOWED_EXTENSIONS))
        logger.error(err)
        return err

    if not fchunk.afile:
        err = utils.pack_error("No file specified.")
        logger.error(err)
        return err

    chunk_path = get_chunk_path(file_name, fchunk.number)

    try:
        # For every request recived we store the chunk to a temp folder
        fchunk.afile.save(chunk_path)
    except:
        logger.error("Problem saving: {}".format(fchunk))
        return utils.pack_error("Unable to save file chunk: {}"
                                .format(fchunk.number))

    # When all chunks are recived we merge them
    if not all_chunks_received(fchunk):
        return utils.jsonify_success('Request completed successfully.')

    # When all chunks are received we merge them
    merge_completed = merge_files(fchunk)
    if merge_completed:
        delete_temp_files(fchunk)
        hash_matches = verify_file_integrity(fchunk)
        if hash_matches:
            return utils.jsonify_success('File {} uploaded successfully.'
                                         .format(file_name))
        else:
            logger.error("md5 sum does not match for: {}".format(fchunk))
            return utils.jsonify_error('Checksum mismatch for file: {}'
                                       .format(file_name))
    else:
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

    :rtype boolean
    :return true if the file was reconstructed from the chunks
    """
    success = False
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

        success = True
        # log_manager.log_file_upload(subject_file)
    except Exception as exc:
        logger.error("There was an issue in merge_files(): {}".format(exc))

    return success
