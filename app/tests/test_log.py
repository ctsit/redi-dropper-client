from datetime import datetime

from redidropper.main import db
from redidropper.models.log_entity import LogEntity, LogTypeEntity
from redidropper.models.log_entity import WebSessionEntity

from .base_test import BaseTestCase


class LogTests(BaseTestCase):

    def test_log_creation(self):
        log_type = LogTypeEntity.create(type='login', description='')
        web_session = WebSessionEntity.create()

        log = LogEntity.create(type_id=log_type.id, ip='8.8.8.8',
                               web_session_id=web_session.id,
                               date_time=datetime.now(),
                               details='just a test')

        db.session.add(log)
        db.session.commit()

        assert log.id == 1
