# Goal: @TODO
#
# @authors:
#   Andrei Sura             <sura.andrei@gmail.com>
#   Ruchi Vivek Desai       <ruchivdesai@gmail.com>
#   Sanath Pasumarthy       <sanath@ufl.edu>
#
# @TODO: fix camelCaseS


import os
import math
import logging

from flask import request
from redidropper.main import app

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
    filename    = request.form['resumableFilename']
    logger.info("Handling request for chunk {} of file: {}" \
            .format(chunkNumber, filename))

    file = request.files['file']

    if not file:
        return "error: no file specified"

    chunk_path = get_chunk_path(filename, chunkNumber)

    try:
        file.save(chunk_path)
    except:
        print "problem with save"

    currentTestChunk = 1

    # can't multiply sequence by non-int of type 'float'
    numberOfChunks = int(max(math.floor(totalSize/chunkSize), 1)) + 1

    # For every request recived we store the chunk to a temp folder
    # until all chunks are ready
    for i in range(1, numberOfChunks):
        chunk_path = get_chunk_path(filename, chunkNumber)
        if os.path.isfile(chunk_path):
            if i == numberOfChunks:
                logger.debug("All {} chunks received for {}.".format(chunkNumber, filename))
                # Join the list of files
                file_manager.merge_files(numberOfChunks, filename)
        else:
            break

    return "success"


def verify_file_integrity(file_props):
    logger.debug("Verify md5sum...")
    pass


def delete_temp_files(file_props):
    logger.debug("Removing file chunks")

    for i in range(1, file_props['num_chunks']):
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
