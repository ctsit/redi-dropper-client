# Goal: @TODO
#
# @authors:
#   Andrei Sura             <sura.andrei@gmail.com>
#   Ruchi Vivek Desai       <ruchivdesai@gmail.com>
#   Sanath Pasumarthy       <sanath@ufl.edu>
#
# @TODO: fix camelCaseS


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

def get_file_path(file_name):
    return os.path.join(app.config['INCOMING_SAVED_DIR'], file_name)


def get_chunk_path(file_name, chunk_number):
    name = "{}.part{}".format(file_name, chunk_number)
    return os.path.join(app.config['INCOMING_TEMP_DIR'], name)


def save_uploaded_file():
    """ Receives files on the server side """

    # @TODO: !!! add size checks for user input
    chunkNumber = int(request.form['resumableChunkNumber'])
    chunkSize   = int(request.form['resumableChunkSize'])
    totalSize   = int(request.form['resumableTotalSize'])
    identifier  = request.form['resumableIdentifier']
    filename    = secure_filename(request.form['resumableFilename'])
    file        = request.files['file']

    # can't multiply sequence by non-int of type 'float'
    numberOfChunks = int(max(math.floor(totalSize/chunkSize), 1))

    logger.info("Uploading chunk {} out of {} for file: {} ({} out of {} bytes)" \
            .format(chunkNumber, numberOfChunks, filename, chunkSize, totalSize))

    if not utils.allowed_file(filename):
        err = utils.pack_error("Invalid file type: {}." \
                "Allowed extensions: {}".format(filename, utils.ALLOWED_EXTENSIONS))
        logger.error(err)
        return err

    if not file:
        err = utils.pack_error("No file specified.")
        logger.error(err)
        return err

    chunk_path = get_chunk_path(filename, chunkNumber)

    try:
        # For every request recived we store the chunk to a temp folder
        file.save(chunk_path)
    except:
        print "problem with save"

    # When all chunks are recived we merge them
    if all_chunks_received(numberOfChunks, filename):
        merge_files(numberOfChunks, filename)

    return "success"


def all_chunks_received(numberOfChunks, filename):
    done = False

    for i in range(1, numberOfChunks + 1):
        chunk_path = get_chunk_path(filename, i)

        if os.path.isfile(chunk_path):
            if i == numberOfChunks:
                logger.debug("Verified all {} chunks received for {}." \
                        .format(numberOfChunks, filename))
                done = True
        else:
            break
    return done


def verify_file_integrity(file_props):
    logger.debug("Verify md5sum...")
    pass


def delete_temp_files(file_props):
    logger.debug("Removing file chunks")

    for i in range(1, file_props['num_chunks'] + 1):
        chunk_path = get_chunk_path(file_props['file_name'], i)
        os.remove(chunk_path)


def merge_files(numberOfChunks, file_name):
    file_path = get_file_path(file_name)
    logger.debug("Saving file: [{}] from [{}]".format(file_name, numberOfChunks))

    f = open(file_path, "w")

    for i in range(1, int(numberOfChunks) + 1):
        chunk_path = get_chunk_path(file_name, i)
        tempfile = open(chunk_path, "r")
        f.write(tempfile.read())

    file_props = {'file_name': file_name, 'num_chunks': int(numberOfChunks)}
    verify_file_integrity(file_props)
    delete_temp_files(file_props)
