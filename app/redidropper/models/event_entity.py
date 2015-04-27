"""
ORM for Event table
"""

from redidropper.main import db
from redidropper.database.crud_mixin import CRUDMixin


class EventEntity(db.Model, CRUDMixin):

    """ Stores a list of redcap events """
    __tablename__ = 'Event'

    id = db.Column("evtID", db.Integer, primary_key=True)
    redcap_arm = db.Column("evtRedcapArm", db.String(255), nullable=False)
    redcap_event = db.Column("evtRedcapEvent", db.String(255), nullable=False)
    added_at = db.Column("evtAddedAt", db.DateTime(), nullable=False,
                         server_default='0000-00-00 00:00:00')
