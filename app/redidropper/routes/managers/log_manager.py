"""
Goal: Implement logs-specific logic

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

def get_logs(project_id, page_num):
    """
    @TODO: implement
    """

    total_pages = 5
    logs = {
            1: [
                {'event_id':'123','username':'test1','timestamp':'20th Jan'},
                {'event_id':'239','username':'test2','timestamp':'20th Jan'},
                {'event_id':'326','username':'test3','timestamp':'20th Jan'},
                {'event_id':'123','username':'test4','timestamp':'20th Jan'}
                ],
            2: [
                {'event_id': '1', 'username':'test1', 'timestamp': 'Jan 1'},
                {'event_id': '2', 'username':'test2', 'timestamp': 'Jan 2'},
                ]
            }
    return (logs[page_num], total_pages)
