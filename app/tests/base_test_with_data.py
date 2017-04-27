"""
Goal: Extend the base test class by inserting samle rows in the database

Authors:
    Akash Agarwal <agarwala989@gmail.com
    Andrei Sura <sura.andrei@gmail.com>

"""

from datetime import datetime
from .base_test import BaseTestCase
from redidropper import utils
from redidropper.main import db

from redidropper.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN, \
    ROLE_RESEARCHER_ONE, ROLE_RESEARCHER_TWO, ROLE_DELETER
from redidropper.models.event_entity import EventEntity
from redidropper.models.user_entity import UserEntity
from redidropper.models.role_entity import RoleEntity
from redidropper.models.subject_entity import SubjectEntity
from redidropper.models.subject_file_entity import SubjectFileEntity
from redidropper.models.log_type_entity import LogTypeEntity
from redidropper.models.user_agent_entity import UserAgentEntity
from redidropper.models.log_type_entity import LOG_TYPE_LOGIN, LOG_TYPE_LOGOUT


class BaseTestCaseWithData(BaseTestCase):

    """ Add data... """

    def setUp(self):
        db.create_all()
        self.create_log_types()
        self.create_user_agents()
        self.create_sample_data()

    def create_log_types(self):
        log_login = LogTypeEntity.create(type=LOG_TYPE_LOGIN, description='')
        log_logout = LogTypeEntity.create(type=LOG_TYPE_LOGOUT, description='')
        self.assertEquals(1, log_login.id)
        self.assertEquals(2, log_logout.id)

    def create_user_agents(self):
        user_agent_string = ""
        hash = utils.compute_text_md5(user_agent_string)
        user_agent = UserAgentEntity.create(user_agent=user_agent_string,
                                            hash=hash,
                                            platform="Linux",
                                            browser="Firefox",
                                            version="latest",
                                            language="EN-US")
        self.assertIsNotNone(user_agent)

    def create_sample_data(self):
        """ Add some data """
        # == Create users
        added_date = datetime.today()
        access_end_date = utils.get_expiration_date(180)
        admin_user = UserEntity.create(email="admin@example.com",
                                 first="First",
                                 last="Last",
                                 minitial="M",
                                 added_at=added_date,
                                 modified_at=added_date,
                                 email_confirmed_at=added_date,
                                 access_expires_at=access_end_date)

        tech_user = UserEntity.create(email="tech@example.com",
                                 first="First",
                                 last="Last",
                                 minitial="T",
                                 added_at=added_date,
                                 modified_at=added_date,
                                 email_confirmed_at=added_date,
                                 access_expires_at=access_end_date)

        # == Create roles
        role_admin = RoleEntity.create(name=ROLE_ADMIN, description='role')
        role_tech = RoleEntity.create(name=ROLE_TECHNICIAN, description='role')
        role_res1 = RoleEntity.create(name=ROLE_RESEARCHER_ONE, description='')
        role_res2 = RoleEntity.create(name=ROLE_RESEARCHER_TWO, description='')
        role_deleter = RoleEntity.create(name=ROLE_DELETER, description='role')
        admin_user.roles.extend([role_admin, role_tech, role_res1, role_res2, role_deleter])
        tech_user.roles.extend([role_tech])

        # == Create subject
        subject = SubjectEntity.create(
            redcap_id="001",
            added_at=added_date,
            last_checked_at=added_date,
            was_deleted=0)

        # == Create events
        evt = EventEntity.create(redcap_arm='Arm 1',
                                 redcap_event='Event 1',
                                 day_offset=1,
                                 added_at=added_date)
        evt2 = EventEntity.create(redcap_arm='Arm 1',
                                  redcap_event='Event 2',
                                  day_offset=2.3,
                                  added_at=added_date)

        self.assertIsNotNone(evt.id)
        self.assertIsNotNone(evt2.id)

        files = [
            {'name': 'a.png', 'size': '123', 'event': evt.id},
            {'name': 'b.png', 'size': '1234', 'event': evt.id},
            {'name': 'c.png', 'size': '12345', 'event': evt2.id},
            {'name': 'd.png', 'size': '123456', 'event': evt2.id},
            {'name': 'e.png', 'size': '1234567', 'event': evt2.id},
        ]

        # Create subject files
        for fdata in files:
            subject_file = SubjectFileEntity.create(
                subject_id=subject.id,
                event_id=fdata['event'],
                file_name=fdata['name'],
                file_type="N/A",
		            file_check_sum=utils.compute_text_md5(fdata['name']),
                file_size=fdata['size'],
                uploaded_at=added_date,
                user_id=admin_user.id)
            self.assertIsNotNone(subject_file.id)
            # app.logger.debug("Init test case with: {}".format(subject_file))
