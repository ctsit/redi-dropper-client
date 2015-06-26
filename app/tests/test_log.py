from datetime import datetime

from redidropper.models.log_type_entity import LOG_TYPE_LOGIN, LOG_TYPE_LOGOUT
from redidropper.models.log_type_entity import LogTypeEntity
from redidropper.models.log_entity import LogEntity
from redidropper.models.web_session_entity import WebSessionEntity

from .base_test import BaseTestCase


class LogTests(BaseTestCase):

    def test_log_creation(self):
        log_login = LogTypeEntity.create(type=LOG_TYPE_LOGIN, description='')
        log_logout = LogTypeEntity.create(type=LOG_TYPE_LOGOUT, description='')
        self.assertEquals(1, log_login.id)
        self.assertEquals(2, log_logout.id)

        web_session = WebSessionEntity.create()
        self.assertEquals(1, web_session.id)

        log = LogEntity.create(type_id=log_login.id,
                               web_session_id=web_session.id,
                               date_time=datetime.now(),
                               details='just a test')
        log2 = LogEntity.create(type_id=log_logout.id,
                                web_session_id=web_session.id,
                                date_time=datetime.now(),
                                details='just a test')

        self.assertEquals(1, log.id)
        self.assertEquals(2, log2.id)
        self.assertEquals(LOG_TYPE_LOGIN, log.log_type.type)
        self.assertEquals(LOG_TYPE_LOGOUT, log2.log_type.type)
        # print(log)
