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
from flask import send_file
from flask import make_response
from flask_login import login_required

# from sqlalchemy.orm.exc import NoResultFound
from redidropper.main import app, db
from redidropper import emails

from redidropper.routes.managers import file_manager, subject_manager, \
    log_manager
from redidropper.utils import get_safe_int, jsonify_error, jsonify_success, \
    get_expiration_date

from redidropper.models.subject_entity import SubjectEntity
from redidropper.models.subject_file_entity import SubjectFileEntity
from redidropper.models.event_entity import EventEntity
from redidropper.models.user_entity import UserEntity
from redidropper.models.role_entity import RoleEntity

from redidropper.routes.users import perm_admin
# , perm_admin_or_technician


@app.route('/api/list_subject_events', methods=['POST', 'GET'])
@login_required
def api_list_subject_events():
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    # from sqlalchemy.sql import text
    from collections import namedtuple

    if 'POST' == request.method:
        subject_id = get_safe_int(request.form.get('subject_id'))
        # = get_safe_int(request.form.get(''))
        # = get_safe_int(request.args.get(''))
    else:
        subject_id = get_safe_int(request.args.get('subject_id'))

    query = """
SELECT
    evtID AS id
    , evtRedcapArm AS redcap_arm
    , evtRedcapEvent AS redcap_event
    , LOWER(
        REPLACE(
            CONCAT(evtRedcapEvent, '_', evtRedcapArm),
            ' ',
            '_')
    ) AS unique_event_name
    , COUNT(sfID) AS total_files
    , GROUP_CONCAT( CONCAT(sfFileName, ':', sfFileSize)) AS file_names
FROM
     Event
    JOIN SubjectFile USING(evtID)
WHERE
    sbjID = :subject_id
GROUP BY
    evtID
    """
    result = db.session.execute(query, {'subject_id': subject_id})
    Event = namedtuple('Event', result.keys())
    events = [Event(*r) for r in result.fetchall()]
    events_ser = [i._asdict() for i in events]
    return jsonify_success({'subject_events': events_ser})


@app.route('/api/list_subject_event_files', methods=['POST', 'GET'])
@login_required
def api_list_subject_event_files():
    """
    :rtype: Response
    :return the list of subjects in json format
    """

    if 'POST' == request.method:
        subject_id = get_safe_int(request.form.get('subject_id'))
        event_id = get_safe_int(request.form.get('event_id'))
        # = get_safe_int(request.form.get(''))
        # = get_safe_int(request.args.get(''))
    else:
        subject_id = get_safe_int(request.args.get('subject_id'))
        event_id = get_safe_int(request.args.get('event_id'))

    # files = SubjectFileEntity.query.filter_by(s.redcap_id=redcap_id).all()
    files = SubjectFileEntity \
        .query.filter_by(subject_id=subject_id,
                         event_id=event_id).all()
    files_ser = [i.serialize() for i in files]
    return jsonify_success({'subject_event_files': files_ser})


@app.route('/api/find_subject', methods=['POST', 'GET'])
def find_subject():
    """
    :rtype: Response
    :return the list of subjects in json format
    """

    if 'POST' == request.method:
        search_id = request.form['name']
    else:
        search_id = request.args.get('name')

    matching = []

    if search_id is not None:
        # @TODO: optimize to return one column by default
        # http://stackoverflow.com/questions/7533146/how-do-i-select-additional-manual-values-along-with-an-sqlalchemy-query
        subject_list = SubjectEntity.query.filter(
            SubjectEntity.redcap_id.like("%{}%".format(search_id))
        ).all()
        matching = [subject.redcap_id for subject in subject_list]
        # matching = [found for found in matching if search_id in found]
    else:
        app.logger.debug("Invalid API call: "
                         "no value provided for redcap_subject_id.")

    return jsonify_success({'subjects': matching})


@app.route('/api/list_events', methods=['POST', 'GET'])
def list_events():
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    # redcap_subject_id = request.form['subject_id']
    # if redcap_subject_id is not None:
    events = EventEntity.query.all()
    events_ser = [i.serialize() for i in events]
    return jsonify_success({'events': events_ser})


@app.route('/api/upload', methods=['POST', 'GET'])
@login_required
def api_upload():
    """ Receives files on the server side
    :rtype: Response
    :return the status of the upload action in json format
    """
    return make_response(file_manager.save_uploaded_file(), 200)


@app.route("/api/download_file", methods=['POST', 'GET'])
@login_required
def download_file():
    """ Download a file using the database id """

    if 'POST' == request.method:
        file_id = request.form['file_id']
    else:
        file_id = request.args.get('file_id')

    # 1 ==> example_1.tgz
    file_path = file_manager.get_file_path_from_id(file_id)
    print "serving file: " + file_path
    return send_file(file_path, as_attachment=True)


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
        return jsonify_error({'message': 'Sorry. This email is already taken.'})

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
    return jsonify_success({'user': user.serialize()})


@app.route('/api/list_users', methods=['POST', 'GET'])
@login_required
def api_list_users():
    """
    @TODo: use the page_num in the query
    :rtype: Response
    :return
    """
    if 'POST' == request.method:
        per_page = get_safe_int(request.form.get('per_page'))
        page_num = get_safe_int(request.form.get('page_num'))
    else:
        per_page = get_safe_int(request.args.get('per_page'))
        page_num = get_safe_int(request.args.get('page_num'))

    # users = UserEntity.query.all()
    # users = UserEntity.query.filter(UserEntity.id >= 14).all()
    pagination = UserEntity.query.paginate(page_num, per_page, False)
    items = [i.serialize() for i in pagination.items]
    return jsonify_success({"total_pages": pagination.pages,
                            "list_of_users": items})


@app.route('/api/list_logs', methods=['GET', 'POST'])
@login_required
def api_list_logs():
    """
    Render the specified page of event logs
    @TODO: show user-specific logs for non-admins?

    :rtype: string
    :return the json list of logs
    """
    if 'POST' == request.method:
        per_page = get_safe_int(request.form.get('per_page'))
        page_num = get_safe_int(request.form.get('page_num'))
    else:
        per_page = get_safe_int(request.args.get('per_page'))
        page_num = get_safe_int(request.args.get('page_num'))

    """
    pagination = LogEntity.query.paginate(page_num, per_page, False)
    items = [i.serialize() for i in pagination.items]
    app.logger.debug("per_page: {}, page_num: {}".format(per_page, page_num))
    return jsonify_success(dict(total_pages=pagination.pages,
                                list_of_events=items))
    """
    logs, total_pages = log_manager.get_logs(per_page, page_num)
    # logs_list = [x.to_visible() for x in logs]
    return jsonify_success(dict(list_of_events=logs, total_pages=total_pages))


@app.route('/api/list_redcap_subjects', methods=['POST', 'GET'])
@login_required
def api_list_redcap_subjects():
    """
    :rtype: Response
    :return the list of subjects in json format
    """
    subjects = subject_manager.get_fresh_list_of_subjects()
    subjects_list = [x.to_visible() for x in subjects]
    return jsonify_success({'subjects_list': subjects_list})


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
    # app.logger.debug("per_page: {}, page_num: {}".format(per_page, page_num))
    return jsonify_success(dict(total_pages=pagination.pages,
                                list_of_subjects=items))


@app.route('/api/activate_account', methods=['POST'])
@perm_admin.require()
def api_activate_account():
    """
    Activate an user.
    @TODO: should change expiration date too?

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = get_safe_int(request.form.get('user_id'))
    user = UserEntity.get_by_id(user_id)
    user = UserEntity.update(user, active=True)
    return jsonify_success({"message": "User activated."})


@app.route('/api/deactivate_account', methods=['POST'])
@perm_admin.require()
def api_deactivate_account():
    """
    De-activate an user.
    @TODO: should change expiration date too?

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = get_safe_int(request.form.get('user_id'))
    user = UserEntity.get_by_id(user_id)
    user = UserEntity.update(user, active=False)
    return jsonify_success({"message": "User deactivated."})


@app.route('/api/send_verification_email', methods=['POST'])
@perm_admin.require()
def api_send_verification_email():
    """
    @TODO: allow POST only
    @TODO: Send Verification Email to user_id

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = get_safe_int(request.form.get('user_id'))
    user = UserEntity.get_by_id(user_id)
    user = UserEntity.get_by_id(1)
    user.email = app.config['MAIL_SENDER_SUPPORT']

    try:
        emails.send_verification_email(user)
        return jsonify_success({"message": "Verification email was sent."})
    except Exception as exc:
        details = "Connection config: {}/{}:{}".format(
            app.config['MAIL_USERNAME'],
            app.config['MAIL_SERVER'],
            app.config['MAIL_PORT'])
        app.logger.debug(details)
        return jsonify_error({"message": "Unable to send email due: {} {}"
                              .format(exc, details)})


@app.route('/api/verify_email', methods=['POST', 'GET'])
def api_verify_email():
    """
    @TODO: add column for verification hash

    :rtype: Response
    :return the success or failed in json format
    """
    token = request.form.get('tok')

    # user = UserEntity.query.filter_by(email_token=token).first()
    user = UserEntity.get_by_id(1)

    if user is None:
        app.logger.error("Attempt to verify email with incorrect token: {}"
                         .format(token))
        return jsonify_error({'message': 'Sorry.'})

    app.logger.debug("Verified token {} for user {}".format(token, user.email))
    # implement update User set usrEmailConfirmedAt = NOW()
    return jsonify_success({"message": "Verification email was sent."})


@app.route('/api/expire_account', methods=['POST'])
@perm_admin.require()
def api_expire_account():
    """
    Change the `User.usrAccessExpiresAt` to today's date and 00:00:00 time
    effectively blocking the user access.

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = get_safe_int(request.form.get('user_id'))
    user = UserEntity.get_by_id(user_id)
    today = datetime.today()
    today_start = datetime(today.year, today.month, today.day)
    user = UserEntity.update(user, access_expires_at=today_start)
    return jsonify_success({"message": "User access was expired."})


@app.route('/api/extend_expiration_date', methods=['POST'])
@perm_admin.require()
def api_extend_expiration_date():
    """
    Change the `User.usrAccessExpiresAt` to today's date + 180 days

    :rtype: Response
    :return the success or failed in json format
    """
    user_id = request.form.get('user_id')
    today_plus_180 = get_expiration_date(180)
    user = UserEntity.get_by_id(user_id)
    user = UserEntity.update(user, access_expires_at=today_plus_180)
    return jsonify_success(
        {"message": "Updated expiration date to {}".format(today_plus_180)})
