"""
Goal: Implement logs-specific logic

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
  Taeber Rapczak          <taeber@ufl.edu>
"""
from redidropper.models.log_entity import LogEntity
from redidropper.main import app

# @TODO: move to log_entity.py
# @TODO: add filters

def get_logs(per_page=25, page_num=1):
    """
    Helper for formating the event details
    """
    def item_from_entity(entity):
        return {
            'id': entity.id,
            'type': entity.log_type.type,
            'details': entity.details,
            'web_session_id': entity.web_session.session_id,
            'web_session_ip': entity.web_session.ip,
            'date_time': entity.date_time,
        }

    pagination = LogEntity.query.paginate(page_num, per_page, False)
    items = map(item_from_entity, pagination.items)
    return items, pagination.pages
