# Goal: @TODO
#
# @authors:
#   Andrei Sura             <sura.andrei@gmail.com>
#   Ruchi Vivek Desai       <ruchivdesai@gmail.com>
#   Sanath Pasumarthy       <sanath@ufl.edu>
#

# bcrypt http://security.stackexchange.com/questions/4781/do-any-security-experts-recommend-bcrypt-for-password-storage/6415#6415
#

import os
import math
import logging

from flask import request
from werkzeug import secure_filename

from redidropper import utils
from redidropper.main import app


logger = app.logger


class FileChunk(object):
    """ Properties storage for a file chunk """

    def __init__(self, request):
        # @TODO: !!! add size checks for user input
        self.number     = int(request.form['resumableChunkNumber'])
        self.size       = int(request.form['resumableChunkSize'])
        self.total_size = int(request.form['resumableTotalSize'])
        self.uniqueid   = request.form['resumableIdentifier']
        self.file_name  = secure_filename(request.form['resumableFilename'])
        self.afile      = request.files['file']
        self.total_parts= int(max(math.floor(self.total_size/self.size), 1))

    def __str__(self):
        return "FileChunk <{} out of {} for file: {} ({} out of {} bytes)>" \
            .format(self.number,
                    self.total_parts,
                    self.file_name,
                    self.size,
                    self.total_size)



def get_chunk_path(file_name, chunk_number):
    name = "{}.part{}".format(file_name, chunk_number)
    return os.path.join(app.config['INCOMING_TEMP_DIR'], name)


def get_file_path(file_name):
    return os.path.join(app.config['INCOMING_SAVED_DIR'], file_name)


def save_uploaded_file():
    """ Receives files on the server side """
    fchunk = FileChunk(request)
    logger.info("Uploading {}".format(fchunk)) 

    file_name = fchunk.file_name

    if not utils.allowed_file(file_name):
        err = utils.pack_error("Invalid file type: {}." \
                "Allowed extensions: {}" \
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
        return utils.pack_error("Unable to save file chunk: {}" \
                .format(fchunk.number))

    # When all chunks are recived we merge them
    if all_chunks_received(fchunk):
        merge_files(fchunk)
        verify_file_integrity(fchunk)
        delete_temp_files(fchunk)
        return utils.pack_info('File {} uploaded successfully.' \
                .format(file_name))
    else:
        return utils.pack_info('Request completed successfully.')


def all_chunks_received(fchunk):
    done = False
    file_name = fchunk.file_name

    for i in range(1, fchunk.total_parts + 1):
        chunk_path = get_chunk_path(file_name, i)

        if os.path.isfile(chunk_path):
            if i == fchunk.total_parts:
                logger.debug("Verified all {} chunks received for {}." \
                        .format(fchunk.total_parts, file_name))
                done = True
        else:
            break
    return done


def verify_file_integrity(fchunk):
    logger.debug("Verify md5sum...")
    pass


def delete_temp_files(fchunk):
    file_name = fchunk.file_name
    logger.debug("Removing {} file chunks for: {}" \
            .format(fchunk.total_parts, file_name))

    for i in range(1, fchunk.total_parts + 1):
        chunk_path = get_chunk_path(file_name, i)
        os.remove(chunk_path)


def merge_files(fchunk):
    file_name = fchunk.file_name
    file_path = get_file_path(file_name)
    logger.debug("Saving file: {} consisting of {} chunks." \
            .format(file_name, fchunk.total_parts))

    f = open(file_path, "w")

    for i in range(1, fchunk.total_parts + 1):
        chunk_path = get_chunk_path(file_name, i)
        tempfile = open(chunk_path, "r")
        f.write(tempfile.read())

def get_file_path_from_id(file_id):
    #get file path from database
    file_path="/Users/sanathkumarpasumarthy/.redidropper/incoming/saved/example.tgz"
    return file_path
