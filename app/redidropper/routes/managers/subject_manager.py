"""
Goal: Implement subject-specific logic

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

from redidropper.main import app, db
from redidropper.models.all import UserEntity

def get_files(subject_id):
    """ Fetch the list of files for the specified subject_id """
    data = [
{"file_name": "123.jpg", "file_added": "today", "file_added_by": "technician 1"},
{"file_name": "xyz.jpg", "file_added": "2015-01-01 01:02:03", "file_added_by": "technician 2"},
{"file_name": "abc.jpg", "file_added": "today", "file_added_by": "technician 3"}
]
    return data


def refresh_redcap_subjects(project_id):
    """
    Communicate with REDCap to get the updated list of subjects
    then insert/delete the new/removed subjects.
    """
    fresh_set = set(get_fresh_list_of_subjects_for_project(project_id))
    stale_set = set(get_stale_list_of_subjects_for_project(project_id))

    new_subjects = list(fresh_set.difference(stale_set))
    deleted_subjects = list(stale_set.difference(fresh_set))

    insert_count = len(insert_subjects(new_subjects))
    delete_count = len(delete_subjects(deleted_subjects))
    return (insert_count, delete_count)


def get_fresh_list_of_subjects_for_project(project_id):
    """ Communicate with REDCap to get the updated list of subjects

    :rtype: list
    :return the subjects in the REDCap database
    """
    data = []
    return data


class SubjectEntity(object):
    """ POPO for Subject table
    @TODO: move to models
    """
    visible_props = ['subjID', 'subjFileCount', 'subjName']

    def __init__(self, project_id, subject_id, file_count):
        """
        Create Subject
        """
        self.prjID = project_id
        self.subjID = subject_id
        self.subjFileCount = file_count
        self.subjName = "Name {}_{}".format(project_id, subject_id)


    @property
    def to_visible(self):
        """
        Helper for exposing only "secure" class attributes as a dictionary
        @see http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
        """
        return dict( [(key, val) for key, val in self.__dict__.items() \
                if key in SubjectEntity.visible_props])


def get_stale_list_of_subjects_for_project(project_id):
    """ Fetch the set of subjects for the specified project_id
    @TODO: implement

    :rtype: list
    :return the subjects in the local database
    """
    data = {
        1: [
            SubjectEntity(project_id, 1, 10),
            SubjectEntity(project_id, 2, 20),
            SubjectEntity(project_id, 3, 30),
        ],
        2: [
            SubjectEntity(project_id, 1, 10),
            SubjectEntity(project_id, 2, 20),
            SubjectEntity(project_id, 3, 30),
            SubjectEntity(project_id, 4, 40),
        ],
        }
    return data[project_id]


def insert_subjects(subjects):
    """
    :param: subjects -- list

    :rtype: integer
    :return the number of subjects inserted in the local database
    """
    for subj in subjects:
        print("Insert {}".format(subj))
    return 0


def delete_subjects(subjects):
    """
    :param: subjects -- list

    :rtype: integer
    :return the number of subjects *marked as deleted* in the local database
    """
    for subj in subjects:
        print("Delete {}".format(subj))
    return 0


def get_project_subjects_on_page(project_id, page_num, per_page):
    """
    @TODO: implement
    """
    total_pages = 3

    if 1 == int(page_num):
        list_of_subjects = [
                {
                'subject_id': '1', 'subject_name': 'Subject 1',
                    'events':[{'event_id': '1', 'event_files': '10'}]
                },
                {
                'subject_id': '2', 'subject_name': 'Subject 2',
                    'events':[{'event_id': '2', 'event_files': '20'}]
                }
            ]
    else:
        list_of_subjects = [
                {
                'subject_id': '1', 'subject_name': 'Subject 1',
                    'events':[{'event_id': '1', 'event_files': '10'}]
                },
                {
                'subject_id': '2', 'subject_name': 'Subject 2',
                    'events':[{'event_id': '2', 'event_files': '20'}]
                },
                       {
                'subject_id': '3', 'subject_name': 'Subject 3',
                    'events':[{'event_id': '3', 'event_files': '30'}]
                }
            ]

    return (total_pages, list_of_subjects)
