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
from flask import jsonify

from managers import file_manager
from managers import subject_manager
from redidropper.main import app

@app.route('/api/list_subject_files/<subject_id>', methods=['POST'])
def list_subject_files(subject_id=None):
    return subject_manager.get_files(subject_id)


@app.route('/api/list_redcap_subjects', methods=['POST'])
def list_redcap_subjects():
    project_id = 1
    return subject_manager.get_redcap_subjects()


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """ Receives files on the server side """
    return file_manager.save_uploaded_file()



@app.route('/api/users/list')
def get_users_in_project():
    data = [{'id':'123','username':'test1','email':'test1@gmail.com','date_added':'20th Jan','role':'admin','email_verified':'1'},
            {'id':'239','username':'test2','email':'test2@gmail.com','date_added':'20th Jan','role':'technician','email_verified':'0'},
            {'id':'326','username':'test3','email':'test3@gmail.com','date_added':'20th Jan','role':'technician','email_verified':'1'},
            {'id':'123','username':'test4','email':'test4@gmail.com','date_added':'20th Jan','role':'researcher','email_verified':'0'}]
    return jsonify(users=data)

@app.route('/api/admin/events/<page_no>')
def get_list_of_events(page_no):
    data = [{'event_id':'123','username':'test1','timestamp':'20th Jan'},
            {'event_id':'239','username':'test2','timestamp':'20th Jan'},
            {'event_id':'326','username':'test3','timestamp':'20th Jan'},
            {'event_id':'123','username':'test4','timestamp':'20th Jan'}]
    return jsonify(list_of_events=data, no_of_pages=10)

@app.route('/api/list_of_files/<event_id>')
def list_of_event_files(event_id):
    data = [{'file_id':'123','file_name':'test1','file_size':'20 Mb'},
            {'file_id':'239','file_name':'test2','file_size':'10 Mb'},
            {'file_id':'326','file_name':'test3','file_size':'30 Mb'},
            {'file_id':'123','file_name':'test4','file_size':'100 Mb'}]
    return jsonify(list_of_files=data,event_created_date="20th Jan")


@app.route('/api/list_of_projects')
def list_of_projects():
    data = [
    	{'project_id':'1','project_name':'1st Project'},
    	{'project_id':'2','project_name':'2nd Project'}]
    return jsonify(list_of_projects=data,max_events=12)


@app.route('/api/list_of_subjects/<page_num>')
def list_of_subjects(page_num):
	project_id = 1
	total_pages, list_of_subjects = get_project_subjects_on_page(project_id, page_num)    
	return jsonify(total_pages=total_pages, list_of_subjects=list_of_subjects)


def get_project_subjects_on_page(project_id, page_num):
	total_pages = 3

	if 1 == int(page_num):
		list_of_subjects = [
				{
				'subject_id': '1', 'subject_name': 'Subject 1',
					'events':[{'event_id': '1', 'event_files': '10'}]
				},
                {
				'subject_id': '2', 'subject_name': 'Subject 2',
					'events':[{'event_id': '2', 'event_files': '20'}]
				}
			]
	else:
		list_of_subjects = [
				{
				'subject_id': '1', 'subject_name': 'Subject 1',
					'events':[{'event_id': '1', 'event_files': '10'}]
				},
                {
				'subject_id': '2', 'subject_name': 'Subject 2',
					'events':[{'event_id': '2', 'event_files': '20'}]
				},
				       {
				'subject_id': '3', 'subject_name': 'Subject 3',
					'events':[{'event_id': '3', 'event_files': '30'}]
				}
			]

 	return (total_pages, list_of_subjects)
