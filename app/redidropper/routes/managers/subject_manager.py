"""
Goal: Implement subject-specific logic

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

# from redidropper.main import app, db


def refresh_redcap_subjects(project_id):
    """
    Communicate with REDCap to get the updated list of subjects
    then insert/delete the new/removed subjects.
    """
    fresh_set = set(get_fresh_list_of_subjects())
    stale_set = set(get_stale_list_of_subjects())

    new_subjects = list(fresh_set.difference(stale_set))
    deleted_subjects = list(stale_set.difference(fresh_set))

    insert_count = len(insert_subjects(new_subjects))
    delete_count = len(delete_subjects(deleted_subjects))
    return (insert_count, delete_count)


def get_fresh_list_of_subjects():
    """ Communicate with REDCap to get the updated list of subjects

    :rtype: list
    :return the subjects in the REDCap database
    """

    data = [
        RedcapSubject(1),
        RedcapSubject(2),
        RedcapSubject(3),
        ]

    return data


class RedcapSubject(object):
    """
    Abstractization for subjects retrived via cURL from REDCap
    """

    def __init__(self, subject_id):
        """ Create Subject """
        self.subjID = subject_id

    @property
    def to_visible(self):
        """
        Helper for exposing only "secure" class attributes as a dictionary
        """
        return dict([(key, val) for key, val in self.__dict__.items()
                    if key in RedcapSubject.visible_props])


def get_stale_list_of_subjects():
    """

    :rtype: list
    :return the subjects in the local database
    """
    data = []
    return data


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
