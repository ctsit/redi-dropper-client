"""
Goal: test insert/search projects
"""

from flask import url_for
from base_test import BaseTestCase
from redidropper.main import app, db
from redidropper.models.project_entity import ProjectEntity
from redidropper import utils


class DaoProjectTest(BaseTestCase):

    def test_find(self):
        proj = ProjectEntity.create(
            prjName = "Project 1",
            prjUrlHost = "http://localhost:1234",
            prjUrlPath = "/redcap",
            prjApiKey = "1234",
            prjAddedAt = utils.get_db_friendly_date_time()
        )
        projects = ProjectEntity.query.all()
        self.assertTrue(len(ordered) == 1)

        proj2 = ProjectEntity(name="Project2", host="localhost:12345", \
            path="/redcap2", api_key="abc")
        db.session.add(proj2)
        db.session.commit()
        ordered = ProjectEntity.query.order_by(ProjectEntity.prjName)
        self.assertTrue(len(ordered) == 2)

        #response = self.client.post(url_for('/api/list_projects'), data={})
        #self.assert_redirects(response, url_for('user role'))
