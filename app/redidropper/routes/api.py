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
from flask_login import login_required

from sqlalchemy.orm.exc import NoResultFound
from redidropper.main import app

from redidropper.routes.managers import file_manager, subject_manager, \
        log_manager
from redidropper.utils import clean_int, pack_error, pack_success_result

from redidropper.models.user_entity import UserEntity
from redidropper.models.user_role_entity import UserRoleEntity
from redidropper.models import dao



@app.route('/api/list_subject_files/<subject_id>', methods=['POST', 'GET'])
@login_required
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



@app.route('/api/list_redcap_subjects', methods=['POST'])
@login_required
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
@login_required
def api_upload():
    """ Receives files on the server side
    :rtype: Response
    :return the status of the upload action in json format
    """
    return make_response(file_manager.save_uploaded_file(), 200)


@app.route('/api/save_user', methods=['POST'])
@login_required
def api_save_user():
    """ Add New User to the database """
    username = request.form.get('uathUsername')
    email = request.form['usrEmail']
    first = request.form['usrFirst']
    last = request.form['usrLast']
    minitial = request.form['usrMI']
    role_name = request.form['rolName']

    email_exists = False if dao.find_user_by_email(email) is None \
            else True

    if email_exists:
        return make_response(
            pack_error("Sorry. This email is already taken."))

    # @TODO: fix hardcoded values
    #password = 'password'
    #salt, hashed_pass = generate_auth(app.config['SECRET_KEY'], password)
    user = UserEntity.create(email=email, first=first, last=last, \
            minitial=minitial,
            password_hash="")
    app.logger.debug("saved user: {}".format(user))

    role = dao.find_role_by_role_name(role_name)

    if role:
        user_role = UserRoleEntity.create(user_id=user.id, role_id=role.id)
        app.logger.debug("saved user role mapping: {}".format(user_role))

    return make_response(pack_success_result(user.serialize()))


@app.route('/api/list_users', methods=['GET', 'POST'])
@login_required
def api_list_users():
    """

    :rtype: Response
    :return
    """
    users = UserEntity.query().all()

    if users is None:
        return make_response(pack_error("no users found"))

    lista = [i.serialize() for i in users]
    return make_response(pack_success_result(lista))


@app.route('/api/admin/events/<page_num>', methods=['GET', 'POST'])
@login_required
def api_list_logs(page_num):
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


@app.route('/api/list_of_files/<event_id>', methods=['GET', 'POST'])
@login_required
def api_list_event_files(event_id):
    """

    :rtype: Response
    :return
    """

    data = [{'file_id':'123','file_name':'test1','file_size':'20 Mb'},
            {'file_id':'239','file_name':'test2','file_size':'10 Mb'},
            {'file_id':'326','file_name':'test3','file_size':'30 Mb'},
            {'file_id':'123','file_name':'test4','file_size':'100 Mb'}]
    return jsonify(list_of_files=data,event_created_date="20th Jan")


@app.route('/api/list_of_projects', methods=['GET', 'POST'])
@login_required
def api_list_projects():
    """

    :rtype: Response
    :return
    """
    data = [
        {'project_id':'1','project_name':'1st Project'},
        {'project_id':'2','project_name':'2nd Project'}]
    return jsonify(list_of_projects=data, max_events=12)


@app.route('/api/list_of_subjects', methods=['GET', 'POST'])
@login_required
def api_list_subjects():
    """
    Render the table of subjects and their file counts

    :rtype: Response
    :return
    """
    project_id = 1
    per_page = request.form.get('per_page')
    page_num = request.form.get('page_num')

    total_pages, list_of_subjects = \
        subject_manager.get_project_subjects_on_page(project_id, \
                                                per_page, page_num)
    return jsonify(total_pages=total_pages, list_of_subjects=list_of_subjects)
