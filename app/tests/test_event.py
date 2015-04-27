"""
Goal: test search event

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

from .base_test_with_data import BaseTestCaseWithData
from redidropper.models.event_entity import EventEntity
from sqlalchemy.orm.exc import MultipleResultsFound


class TestSevent(BaseTestCaseWithData):

    def test_default_events(self):
        evt = EventEntity.get_by_id(1)
        self.assertIsNotNone(evt)
        self.assertEquals("Event 1", evt.redcap_event)

        with self.assertRaises(MultipleResultsFound):
            evt2 = EventEntity.query.filter_by(redcap_arm='Arm 1').one()

        evt2 = EventEntity.query.filter_by(redcap_arm='Arm 1',
                                           redcap_event='Event 2').one()
        self.assertEquals(2, evt2.id)
