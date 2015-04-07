
def get_files(subject_id):
    return """[
{"file_name": "123.jpg", "file_added": "today", "file_added_by": "technician 1"},
{"file_name": "xyz.jpg", "file_added": "2015-01-01 01:02:03", "file_added_by": "technician 2"},
{"file_name": "abc.jpg", "file_added": "today", "file_added_by": "technician 3"}
]"""


def get_redcap_subjects():
    return """[
{ "id": "1", "name": "Billy Joe", "files": "3"},
{ "id": "002", "name": "Anne Blue", "files": "1"},
{ "id": "200", "name": "Maggie Magic", "files": "10"}
]"""
