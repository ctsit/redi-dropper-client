"""
Goal: Simulate api calls

Authors:
    Akash Agarwal <agarwala989@gmail.com
    Patrick White <pfwhite9@gmail.com> <pfwhite@ufl.edu>

"""

from __future__ import print_function

from flask import url_for
from .base_test_with_data import BaseTestCaseWithData
from redidropper.main import app
from redidropper.main import db
from datetime import datetime

from redidropper import utils
from redidropper.models.user_entity import UserEntity
from redidropper.models.event_entity import EventEntity
from redidropper.models.subject_entity import SubjectEntity
from redidropper.models.subject_file_entity import SubjectFileEntity
import json

class TestAPI(BaseTestCaseWithData):

    """ This is the class that tests the api """

    def __login(self, email):
        return self.client.post("/", data={
            'email': email,
            'password': 'garbagegarbage'
        })

    def test_save_user_no_login(self):
        response = self.client.post("/api/save_user", data={})
        self.assertEqual(response._status_code, 302)

    def test_save_user_no_admin_login(self):
        res_login = self.__login("tech@example.com")
        response = self.client.post("/api/save_user", data={})
        #TODO: fix the 302 error to be a 403 forbidden error
        self.assertEqual(response._status_code, 302)
        #self.assertEqual(response._status_code, 403)

    def test_save_user(self):
        """ Verify that we can save a new user"""
        res_login = self.__login("admin@example.com")
        #build request
        new_user = {
            'email': "test@test.com",
            'first': "john",
            'last': "doe",
            'minitial': "f",
            'roles': ["admin", "technician"],
            'isEdit': False,
        }
        existing_user = UserEntity.query.filter_by(email=new_user['email'])
        if existing_user.count() is 0:
            response = self.client.post("/api/save_user", data=new_user)
            self.assertEqual(response._status_code, 200)
            created_user = UserEntity.query.filter_by(email=new_user['email'])
            self.assertEqual(created_user.count(), 1)
        else:
            self.fail('user already existed')
        print('save user test')

    def test_edit_user(self):
        """ Verify that we can edit an existing user"""
        res_login = self.__login("admin@example.com")
        my_user = {
            'email': "test@test.com",
            'first': "john",
            'last': "doe",
            'minitial': "f",
            'roles': ["admin", "technician"],
            'isEdit': False,
            'usrId': 3,
        }
        sres = self.client.post("/api/save_user", data=my_user)
        existing_user = UserEntity.query.filter_by(email=my_user['email'])
        if existing_user.count() is 1:
            edited_user = my_user
            edited_user['first'] = 'bill'
            response = self.client.post("/api/edit_user", data=edited_user)
            self.assertEqual(response._status_code, 200)
            #see if changed
            after_edit_user = UserEntity.query.filter_by(email=my_user['email'])
            self.assertEqual(after_edit_user.one().first, 'bill')
        else:
            self.fail('user not existing')
        print('edit user test')

    def test_update_fileType(self):
        """ Verify that we can change file type"""
        res_login = self.__login("admin@example.com")

        added_date = datetime.today()
        subject = SubjectEntity.create(
            redcap_id="002",
            added_at=added_date,
            last_checked_at=added_date,
            was_deleted=0)

        # == Create events
        evt = EventEntity.create(redcap_arm='Arm 2',
                                 redcap_event='Event 2',
                                 day_offset=1,
                                 added_at=added_date)

        files = [
            {'name': 'x.png', 'size': '123', 'event': evt.id},
            {'name': 'y.png', 'size': '1234', 'event': evt.id}
        ]

        for fdata in files:
            subject_file = SubjectFileEntity.create(
                subject_id=subject.id,
                event_id=fdata['event'],
                file_name=fdata['name'],
                file_type="N/A",
        file_check_sum=utils.compute_text_md5(fdata['name']),
                file_size=fdata['size'],
                uploaded_at=added_date,
                user_id='1')

        file_entity = SubjectFileEntity.query.filter_by(file_name='x.png').one()
        postdata = {'file_id': file_entity.id, 'file_type': 'MRI'}
        response = self.client.post("/api/update_fileType", data=postdata)
        self.assertEqual(response._status_code, 200)

        after_edit_file = SubjectFileEntity.query.filter_by(file_name='x.png').one()
        self.assertEqual(after_edit_file.file_type, "MRI")
        print('update file test')

    def test_all_files_info(self):
        response = self.client.get("/api/all_files_info")
        self.assertEqual(response._status_code, 200)
        jsondata = json.loads(response.data)
        self.assertGreater(len(jsondata['data']['list_of_files']),1)

    def __get_file_list_data(self, response):
        d = Decoder()
        data = d.decode(response.data)
        return data.get('data').get('subject_event_files')
