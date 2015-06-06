from datetime import datetime

# from redidropper.main import db
from redidropper.models.log_type_entity import LogTypeEntity
from redidropper.models.log_entity import LogEntity
from redidropper.models.web_session_entity import WebSessionEntity

from .base_test import BaseTestCase


class LogTests(BaseTestCase):

    def test_log_creation(self):
        log_type = LogTypeEntity.create(type='login', description='')
        self.assertEquals(1, log_type.id)
        # print(log_type)

        web_session = WebSessionEntity.create()
        self.assertEquals(1, web_session.id)

        log = LogEntity.create(type_id=log_type.id,
                               web_session_id=web_session.id,
                               date_time=datetime.now(),
                               details='just a test')

        self.assertEquals(1, log.id)
        self.assertEquals("login", log.log_type.type)
        # print(log)
