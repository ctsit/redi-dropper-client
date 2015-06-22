"""
Goal: Implement logs-specific logic

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""
from redidropper.models.log_entity import LogEntity
from redidropper.main import app

from collections import namedtuple

# <td>{record.event_id}</td>
# <td>{record.username}</td>
# <td>{record.timestamp}</td>
from redidropper.models.user_entity import UserEntity


def get_logs(per_page=10, page_num=1):
    def item_from_entity(entity):
        return {
            'event_id': "{} - {} - {}".format(entity.id, entity.log_type.type,
                                              entity.details),
            'username': entity.web_session.session_id,
            'timestamp': entity.date_time
        }

    pagination = LogEntity.query.paginate(page_num, per_page, False)
    items = map(item_from_entity, pagination.items)
    app.logger.debug("per_page: {}, page_num: {}".format(per_page, page_num))
    return items, pagination.pages
