"""
Goal: test insert/search projects
"""

from .base_test import BaseTestCase
from redidropper.main import db
from redidropper.models.project_entity import ProjectEntity
import datetime


class DaoProjectTest(BaseTestCase):
    """ test basic operations for ProjectEntity object """

    def get_proj2(self):
        proj2 = ProjectEntity.create(
            name="Project 2",
            url_host="localhost:12345",
            url_path="/redcap2",
            api_key="abc",
            modified_at=datetime.datetime.today())
        return proj2


    def test_find(self):
        """ verify save and find operations """
        proj = ProjectEntity(
            name="Project 1",
            url_host="http://localhost:1234",
            url_path="/redcap",
            api_key="1234",
            added_at=datetime.datetime.today(),
            modified_at=datetime.datetime.today()
        )

        db.session.add(proj)
        # before commit the primary key does not exist
        assert proj.id is None

        # after commit the primary key is generated
        db.session.commit()
        assert 1 == proj.id

        projects = ProjectEntity.query.all()
        assert len(projects) == 1

        # test usage of CRUDMixin.get_by_id() and create()
        proj2 = self.get_proj2()
        assert 2 == proj2.id

        ordered = ProjectEntity.query.order_by(ProjectEntity.name).all()
        # verify that we have two rows now
        assert 2 == len(ordered)

        # verify that the attribute is saved
        first = ordered[0]
        assert "Project 1" == first.name

        # verify that sorting worked
        first = ProjectEntity.query.order_by(db.desc(ProjectEntity.name)) \
                .first()
        assert "Project 2" == first.name


    def test_view_projects(self):
        """ @TODO: add test for viewing saved project in the UI """
        proj = self.get_proj2()

        #from flask import url_for
        #response = self.client.post(url_for('/api/list_projects'), data={})
        #self.assert_redirects(response, url_for('user role'))
