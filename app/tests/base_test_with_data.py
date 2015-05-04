"""
Goal: Extend the base test class by inserting samle rows in the database

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

from datetime import datetime
from .base_test import BaseTestCase
from redidropper import utils
from redidropper.main import app, db
from redidropper.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN, \
    ROLE_RESEARCHER_ONE, ROLE_RESEARCHER_TWO
from redidropper.models.event_entity import EventEntity
from redidropper.models.user_entity import UserEntity
from redidropper.models.role_entity import RoleEntity
from redidropper.models.subject_entity import SubjectEntity
from redidropper.models.subject_file_entity import SubjectFileEntity


class BaseTestCaseWithData(BaseTestCase):

    """ Add data... """

    def setUp(self):
        db.create_all()
        self.create_sample_data()

    def create_sample_data(self):
        """ Add some data """

        # == Create users
        added_date = datetime.today()
        access_end_date = utils.get_expiration_date(180)
        user = UserEntity.create(email="admin@example.com",
                                 first="First",
                                 last="Last",
                                 minitial="M",
                                 added_at=added_date,
                                 modified_at=added_date,
                                 access_expires_at=access_end_date)

        # == Create roles
        role_admin = RoleEntity.create(name=ROLE_ADMIN, description='role')
        role_tech = RoleEntity.create(name=ROLE_TECHNICIAN, description='role')
        user.roles.extend([role_admin, role_tech])

        # == Create subject
        subject = SubjectEntity.create(
            redcap_id="001",
            added_at=added_date,
            last_checked_at=added_date,
            was_deleted=0)

        # == Create events
        evt = EventEntity.create(redcap_arm='Arm 1', redcap_event='Event 1',
                          added_at=added_date)
        evt2 = EventEntity.create(redcap_arm='Arm 1', redcap_event='Event 2',
                           added_at=added_date)

        assert evt.id is not None

        files = [
            {'name': 'a.png', 'size': '1MB', 'event': evt.id},
            {'name': 'b.png', 'size': '2MB', 'event': evt.id},
            {'name': 'c.png', 'size': '3MB', 'event': evt2.id},
            {'name': 'd.png', 'size': '4MB', 'event': evt2.id},
            {'name': 'e.png', 'size': '5MB', 'event': evt2.id},
        ]

        # Create subject files
        for fdata in files:
            subject_file = SubjectFileEntity.create(
                subject_id=subject.id,
                event_id=fdata['event'],
                file_name=fdata['name'],
                file_check_sum=utils.compute_text_md5(fdata['name']),
                file_size=fdata['size'],
                uploaded_at=added_date,
                user_id=user.id)
            app.logger.debug("Init test case with: {}".format(subject_file))
