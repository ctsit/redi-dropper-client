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
from flask import make_response
from flask import jsonify
from flask import make_response

from redidropper.routes.managers import file_manager, subject_manager, \
        log_manager
from redidropper.main import app

from redidropper.utils import clean_int, pack_error, pack_success_result
from redidropper.models.all import UserEntity
from redidropper.models.all import UserAuthEntity
from redidropper.models import dao



@app.route('/api/list_subject_files/<subject_id>', methods=['POST', 'GET'])
def api_list_subject_files(subject_id=None):
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    subject_id = clean_int(subject_id)
    if subject_id is None:
        return make_response(pack_error("invalid subject id"))

    data = subject_manager.get_files(subject_id)
    return jsonify(data)


@app.route('/api/list_subject_files/<subject_id>', methods=['POST'])
def list_subject_files(subject_id=None):
    return subject_manager.get_files(subject_id)


@app.route('/api/list_redcap_subjects', methods=['POST'])
def api_list_redcap_subjects():
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    project_id = 1
    subjects = subject_manager.get_stale_list_of_subjects_for_project(project_id)
    subjects_list = [x.to_visible() for x in subjects]
    return jsonify(data=subjects_list)


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """ Receives files on the server side
    :rtype: Response
    :return the status of the upload action in json format
    """
    return make_response(file_manager.save_uploaded_file(), 200)

@app.route('/api/save_user', methods=['POST'])
def api_save_user():
    """ Add New User to the database """
    usrName = request.form['username']
    usrEmail = request.form['user_email']
    usrFirst = request.form['user_first_name']
    usrLast = request.form['user_last_name']
    usrMI =  request.form['user_middle_name']
    usrRole = request.form['user_role']

    exists = False if dao.find_user_by_email(usrEmail) is None else True
    if exists:
        return make_response(
            pack_error("Sorry. This email is already taken"))


    exists = False if dao.find_auth_by_username(usrName) is None else True

    if exists:
        return make_response(
            pack_error("Sorry. This Username is already taken"))

    user = UserEntity(usrEmail, usrFirst, usrLast, usrMI)
    usrID = dao.save_user(user)

    userAuth = UserAuthEntity(usrID,usrName)
    usrID = dao.save_username(userAuth)

    print "saved user: {}".format(user)
    return jsonify(pack_success_result(user.usrID))

@app.route('/api/users/list')
def api_get_users_in_project():
    """

    :rtype: Response
    :return
    """
    data = [{'id':'123','username':'test1','email':'test1@gmail.com','date_added':'20th Jan','role':'admin','email_verified':'1'},
            {'id':'239','username':'test2','email':'test2@gmail.com','date_added':'20th Jan','role':'technician','email_verified':'0'},
            {'id':'326','username':'test3','email':'test3@gmail.com','date_added':'20th Jan','role':'technician','email_verified':'1'},
            {'id':'123','username':'test4','email':'test4@gmail.com','date_added':'20th Jan','role':'researcher','email_verified':'0'}]
    return jsonify(users=data)


@app.route('/api/admin/events/<page_num>')
def list_logs(page_num):
    """

    :rtype: Response
    :return
    """
    page_num = clean_int(page_num)
    if page_num is None:
        return make_response(pack_error("invalid page number"))

    project_id = 1
    logs, total_pages = log_manager.get_logs(project_id, page_num)
    #logs_list = [x.to_visible() for x in logs]
    return jsonify(list_of_events = logs, total_pages=total_pages)


@app.route('/api/list_of_files/<event_id>')
def list_event_files(event_id):
    """

    :rtype: Response
    :return
    """

    data = [{'file_id':'123','file_name':'test1','file_size':'20 Mb'},
            {'file_id':'239','file_name':'test2','file_size':'10 Mb'},
            {'file_id':'326','file_name':'test3','file_size':'30 Mb'},
            {'file_id':'123','file_name':'test4','file_size':'100 Mb'}]
    return jsonify(list_of_files=data,event_created_date="20th Jan")


@app.route('/api/list_of_projects')
def list_projects():
    """

    :rtype: Response
    :return
    """
    data = [
        {'project_id':'1','project_name':'1st Project'},
        {'project_id':'2','project_name':'2nd Project'}]
    return jsonify(list_of_projects=data, max_events=12)


@app.route('/api/list_of_subjects/<page_num>')
def list_subjects(page_num):
    """

    :rtype: Response
    :return
    """
    project_id = 1
    total_pages, list_of_subjects = subject_manager.get_project_subjects_on_page(project_id, page_num)
    return jsonify(total_pages=total_pages, list_of_subjects=list_of_subjects)
