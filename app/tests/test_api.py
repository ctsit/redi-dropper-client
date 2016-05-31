"""
Goal: Simulate api calls

Authors:
    Patrick White <pfwhite9@gmail.com> <pfwhite@ufl.edu>

"""

from __future__ import print_function

from flask import url_for
from .base_test_with_data import BaseTestCaseWithData
from redidropper.main import app
from redidropper.main import db

from redidropper.models.user_entity import UserEntity

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
        res_login = self.__login("tech@admin")
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
