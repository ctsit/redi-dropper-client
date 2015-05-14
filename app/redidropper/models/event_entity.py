"""
ORM for Event table
"""

from redidropper.main import db
from redidropper.utils import dump_datetime
from redidropper.database.crud_mixin import CRUDMixin


class EventEntity(db.Model, CRUDMixin):

    """ Stores a list of redcap events """
    __tablename__ = 'Event'

    id = db.Column("evtID", db.Integer, primary_key=True)
    redcap_arm = db.Column("evtRedcapArm", db.String(255), nullable=False)
    redcap_event = db.Column("evtRedcapEvent", db.String(255), nullable=False)
    day_offset = db.Column("evtDayOffset", db.Float, nullable=False,
                           server_default='0')
    added_at = db.Column("evtAddedAt", db.DateTime(), nullable=False,
                         server_default='0000-00-00 00:00:00')

    def get_unique_event_name(self):
        """ Helper for generating the unique string `event_arm` """
        uniq = "{}_{}".format(self.redcap_event, self.redcap_arm)
        return uniq.lower().replace(" ", "_")

    def __repr__(self):
        return """<EventEntity (evtID: {0.id},
        evtRedcapArm: {0.redcap_arm}, evtRedcapEvent: {0.redcap_event},
        evtDayOffset: {0.day_offset}, evtAddedAt:{0.added_at})>""".format(self)

    def serialize(self):
        """Return object data for jsonification """

        return {
            'id': self.id,
            'redcap_arm': self.redcap_arm,
            'redcap_event': self.redcap_event,
            'day_offset': self.day_offset,
            'unique_event_name': self.get_unique_event_name(),
            'added_at': dump_datetime(self.added_at),
        }
