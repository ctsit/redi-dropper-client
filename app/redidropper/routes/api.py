"""
Goal: Delegate requests to the `/api` path to the appropriate controller

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

from flask import request
from flask import url_for
from flask import redirect
from flask_user import login_required, roles_required

from managers import file_manager
from managers import subject_manager
from redidropper.main import app

@app.route('/api/list_subject_files', methods=['POST', 'GET'])
def list_subject_files(subject_id):
    return subject_manager.get_files(subject_id)


@app.route('/api/list_redcap_subjects', methods=['POST', 'GET'])
def list_redcap_subjects():
    return subject_manager.get_redcap_subjects()


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """ Receives files on the server side """
    return file_manager.save_uploaded_file()
