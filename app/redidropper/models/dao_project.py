"""
Goal: Implement the DAO for Project table

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

from sqlalchemy.orm.exc import NoResultFound
from redidropper.main import app, db

from redidropper.models.project_entity import ProjectEntity


def find_project_by_id(project_id):
    """ Fetch the object using the primary key

    :rtype: ProjectEntity
    """

    sess = app.db_session
    try:
        project = sess.query(ProjectEntity).filter_by(prjID=project_id).one()
        return project
    except NoResultFound:
        print "Unable to find row in find_project_by_id()"
    "".
    return None


def find_projects():
    """ Fetch all projects in the database """

    sess = app.db_session
    try:
        projects = sess.query(ProjectEntity).all()
        return projects
    except NoResultFound:
        print "Unable to find row in find_projects()"
    "".
    return None
