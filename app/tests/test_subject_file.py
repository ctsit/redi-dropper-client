"""
Goal: test insert/search subject, subject file

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

from .base_test import BaseTestCase
from redidropper.main import db
from redidropper import utils

from redidropper.models.event_entity import EventEntity
from redidropper.models.user_entity import UserEntity
from redidropper.models.subject_entity import SubjectEntity
from redidropper.models.subject_file_entity import SubjectFileEntity
from datetime import datetime


class TestSubjectFile(BaseTestCase):

    """ test basic operations """

    def test_subject(self):
        """ verify save and find operations """

        added_date = datetime.today()
        subject = SubjectEntity.create(
            redcap_id="001",
            added_at=added_date,
            last_checked_at=added_date,
            was_deleted=0)

        self.assertEquals(1, subject.id)
        self.assertEquals("001", subject.redcap_id)

        subjects = SubjectEntity.query.all()
        self.assertEquals(1, len(subjects))

        # test usage of CRUDMixin.get_by_id() and create()
        subject = SubjectEntity.update(subject, redcap_id="002")
        self.assertEquals("002", subject.redcap_id)

        evt = EventEntity.create(redcap_arm='Arm 1', redcap_event='Event 1',
                                 added_at=added_date)

        fdata = {'name': 'a.png', 'size': '1MB', 'event': evt.id}
        user = UserEntity.create(email="admin@example.com",
                                 first="",
                                 last="",
                                 minitial="",
                                 added_at=added_date,
                                 modified_at=added_date,
                                 access_expires_at=added_date)

        subject_file = SubjectFileEntity.create(
            subject_id=subject.id,
            event_id=fdata['event'],
            file_name=fdata['name'],
            file_check_sum=utils.compute_text_md5(fdata['name']),
            uploaded_at=added_date,
            user_id=user.get_id())
        self.assertIsNotNone(subject_file.id)

        actual_count = SubjectFileEntity.query.count()
        self.assertEqual(1, actual_count)

        actual_count = SubjectFileEntity.query.filter_by(
            event_id=1).count()
        self.assertEqual(1, actual_count)

        sfile = SubjectFileEntity.query.first()
        self.assertEqual(user.id, sfile.user_id)
