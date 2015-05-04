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
    added_at = db.Column("evtAddedAt", db.DateTime(), nullable=False,
                         server_default='0000-00-00 00:00:00')

    def get_unique_event_name(self):
        """ Helper for generating the unique string `event_arm` """
        uniq = "{}_{}".format(self.redcap_event, self.redcap_arm)
        return uniq.lower().replace(" ", "_")


    def serialize(self):
        """Return object data for jsonification """

        return {
            'id': self.id,
            'redcap_arm': self.redcap_arm,
            'redcap_event': self.redcap_event,
            'unique_event_name': self.get_unique_event_name(),
            'added_at': dump_datetime(self.added_at),
        }
