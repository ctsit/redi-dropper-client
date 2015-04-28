"""
Goal: Delegate requests to the `/api` path to the appropriate controller

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

import math
from datetime import datetime
from flask import request
from flask import make_response
from flask import jsonify
from flask_login import login_required

# from sqlalchemy.orm.exc import NoResultFound
from redidropper.main import app

from redidropper.routes.managers import file_manager, subject_manager, \
    log_manager
from redidropper.utils import get_safe_int, pack_error, pack_success_result, \
    get_expiration_date

from redidropper.models.subject_entity import SubjectEntity
from redidropper.models.subject_file_entity import SubjectFileEntity
from redidropper.models.user_entity import UserEntity
from redidropper.models.role_entity import RoleEntity


@app.route('/api/list_subject_files', methods=['POST', 'GET'])
@app.route('/api/list_subject_files/<int:subject_id>', methods=['POST', 'GET'])
@login_required
def api_list_subject_files(subject_id=None):
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    # return make_response(pack_error("invalid subject id"))
    data = subject_manager.get_files(subject_id)
    return jsonify(data)


def search_subject(redcap_subject_id):
    """ TODO: execute a query here """
    subject_list = ['a', 'dgc', 'bcd', 'ab', 'abc', 'bac', 'cad']
    matching = [s for s in subject_list if redcap_subject_id in s]
    return matching


@app.route('/api/find_subject', methods=['POST'])
def find_subject():
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    redcap_subject_id = request.form['name']
    data = search_subject(redcap_subject_id)
    return jsonify(data=data)


def search_events(redcap_subject_id):
    """ @TODO: implement """
    data = {
        "a": [1, 2, 3],
        "ab": [1, 2, 3, 4],
        "abc": [1, 2, 3, 4],
        "bac": [1, 2],
        "bcd": [1, 2, 3, 4, 5],
    }
    return data[redcap_subject_id]


@app.route('/api/list_events', methods=['POST', 'GET'])
def list_events():
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    redcap_subject_id = request.form['subject_id']
    data = search_events(redcap_subject_id)
    return jsonify(data=data)


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
    email = request.form['email']
    first = request.form['first']
    last = request.form['last']
    minitial = request.form['minitial']
    roles = request.form.getlist('roles[]')

    app.logger.debug("roles: {}".format(roles))

    email_exists = False
    try:
        existing_user = UserEntity.query.filter_by(email=email).one()
        email_exists = existing_user is not None
    except:
        pass

    if email_exists:
        return make_response(
            pack_error("Sorry. This email is already taken."))

    # @TODO: fix hardcoded values
    # password = 'password'
    # salt, hashed_pass = generate_auth(app.config['SECRET_KEY'], password)
    added_date = datetime.today()
    access_end_date = get_expiration_date(180)

    user = UserEntity.create(email=email,
                             first=first,
                             last=last,
                             minitial=minitial,
                             added_at=added_date,
                             modified_at=added_date,
                             access_expires_at=access_end_date,
                             password_hash="")
    # roles=user_roles)
    user_roles = []
    try:
        for role_name in roles:
            role_entity = RoleEntity.query.filter_by(name=role_name).one()
            user_roles.append(role_entity)
    except Exception as exc:
        app.logger.debug("Problem saving user: {}".format(exc))

    [user.roles.append(rol) for rol in user_roles]
    user = UserEntity.save(user)
    app.logger.debug("saved user: {}".format(user))
    return make_response(pack_success_result(user.serialize()))


@app.route('/api/list_users', methods=['POST', 'GET'])
@login_required
def api_list_users():
    """
    @TODo: use the page_num in the query
    :rtype: Response
    :return
    """
    per_page = get_safe_int(request.form.get('per_page'))
    page_num = get_safe_int(request.form.get('page_num'))
    app.logger.debug("Show page {} of users".format(page_num))

    users = UserEntity.query.all()
    # users = UserEntity.query.filter(UserEntity.id >= 14).all()

    if users is None:
        return make_response(pack_error("no users found"))

    list_of_users = [i.serialize() for i in users]
    total_pages = math.ceil(len(list_of_users)/float(per_page))
    data = {"total_pages": total_pages, "list_of_users": list_of_users}
    return make_response(pack_success_result(data))


@app.route('/api/list_logs', methods=['GET', 'POST'])
@login_required
def api_list_logs():
    """
    Render the specified page of event logs
    @TODO: show user-specific logs for non-admins?

    :rtype: string
    :return the json list of logs
    """
    per_page = get_safe_int(request.form.get('per_page'))
    page_num = get_safe_int(request.form.get('page_num'))
    logs, total_pages = log_manager.get_logs(per_page, page_num)
    # logs_list = [x.to_visible() for x in logs]
    return jsonify(list_of_events=logs, total_pages=total_pages)


@app.route('/api/list_of_files', methods=['GET', 'POST'])
@app.route('/api/list_of_files/<event_id>', methods=['GET', 'POST'])
@login_required
def api_list_event_files(event_id=1):
    """

    :rtype: Response
    :return
    """

    data = [{'file_id': '123', 'file_name': 'test1', 'file_size': '20 Mb'},
            {'file_id': '239', 'file_name': 'test2', 'file_size': '10 Mb'},
            {'file_id': '326', 'file_name': 'test3', 'file_size': '30 Mb'},
            {'file_id': '123', 'file_name': 'test4', 'file_size': '100 Mb'}]
    return jsonify(list_of_files=data, event_created_date="20th Jan")


@app.route('/api/list_redcap_subjects', methods=['POST', 'GET'])
@login_required
def api_list_redcap_subjects():
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    subjects = subject_manager.get_stale_list_of_subjects()
    subjects_list = [x.to_visible() for x in subjects]
    return jsonify(data=subjects_list)


@app.route('/api/list_local_subjects', methods=['GET', 'POST'])
@login_required
def api_list_local_subjects():
    """
    Render the table of subjects and their file counts

    @see http://pythonhosted.org/Flask-SQLAlchemy/api.html
        #flask.ext.sqlalchemy.BaseQuery.paginate
    paginate(page, per_page=20, error_out=True)

    :rtype: Response
    :return json
    """
    if 'POST' == request.method:
        per_page = get_safe_int(request.form.get('per_page'))
        page_num = get_safe_int(request.form.get('page_num'))
    else:
        per_page = get_safe_int(request.args.get('per_page'))
        page_num = get_safe_int(request.args.get('page_num'))

    pagination = SubjectEntity.query.paginate(page_num, per_page, False)
    items = [i.serialize() for i in pagination.items]
    app.logger.debug("per_page: {}, page_num: {}".format(per_page, page_num))
    return jsonify(total_pages=pagination.pages,
                   list_of_subjects=items)


@app.route('/api')
def api():
    """ Display the list of valid paths under /api/ """

    html = """
<html>
<h2> List of API calls </h2>
<ol>

<li> Logs: <a href="https://localhost:5000/api/list_logs?per_page=5&page_num=1">
        /api/list_logs?per_page=5&page_num=1</a>

<li> Files (for an event): <a href="https://localhost:5000/api/list_of_files/1">
        /api/list_of_files/1</a>

<li> Subjects: <a href="https://localhost:5000/api/list_of_subjects?per_page=1">
        /api/list_of_subjects?per_page=1</a>
</ol>
</html>
    """
    return make_response(html)
