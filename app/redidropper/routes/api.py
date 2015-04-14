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

from sqlalchemy.orm.exc import NoResultFound
from redidropper.main import app, db, db_session as sess

from redidropper.routes.managers import file_manager, subject_manager, \
        log_manager
from redidropper.main import app

from redidropper.utils import clean_int, pack_error, pack_success_result, \
        generate_auth
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
    username = request.form['username']
    email = request.form['user_email']
    first = request.form['user_first_name']
    last = request.form['user_last_name']
    minitial =  request.form['user_middle_name']
    role = request.form['user_role']

    email_exists = False if dao.find_user_by_email(email) is None \
            else True
    username_exists = False if dao.find_auth_by_username(username) is None \
            else True

    if email_exists:
        return make_response(
            pack_error("Sorry. This email is already taken."))

    if username_exists:
        return make_response(
            pack_error("Sorry. This username is already taken."))

    user = UserEntity(email=email, first=first, last=last, minitial=minitial)
    user_id = dao.save_user(user)
    app.logger.debug("saved user: {}".format(user))

    password = 'password'
    salt, hashed_pass = generate_auth(app.config['SECRET_KEY'], password)
    auth = UserAuthEntity(user_id=user_id, username=username, salt=salt, \
            password=hashed_pass)
    uath_id = dao.save_username(auth)
    app.logger.debug("saved auth: {}".format(auth))
    return make_response(pack_success_result(user.usrID))


@app.route('/api/list_users')
def api_get_users_in_project():
    """

    :rtype: Response
    :return
    """
    project_id = 1
    users = dao.find_users_for_project(project_id)

    if users is None:
        return make_response(pack_error("no users found"))

    lista = [i.serialize for i in users]
    return make_response(pack_success_result(lista))


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
