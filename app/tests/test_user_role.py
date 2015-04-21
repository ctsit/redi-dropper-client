"""
Goal: test insert/search projects
"""

from .base_test import BaseTestCase
from redidropper.main import db
from redidropper import utils

from redidropper.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN
from redidropper.models.user_entity import UserEntity
from redidropper.models.role_entity import RoleEntity
from redidropper.models.user_role_entity import UserRoleEntity
from datetime import datetime


class TestUserRole(BaseTestCase):
    """ test basic operations for User, Role, UserRole entities """

    def get_role(self, role):
        """ helper for creating roles """
        roles = {
            ROLE_ADMIN: RoleEntity(name=ROLE_ADMIN,
                                   description='role'),
            ROLE_TECHNICIAN: RoleEntity(name=ROLE_TECHNICIAN,
                                        description='role'),
        }
        return roles[role]

    def test_role(self):
        """ verify save and find operations """
        role_admin = self.get_role(ROLE_ADMIN)
        role_tech = self.get_role(ROLE_TECHNICIAN)

        db.session.add(role_admin)
        # before commit the primary key does not exist
        assert role_admin.id is None

        # after commit the primary key is generated
        db.session.commit()
        assert 1 == role_admin.id

        roles = RoleEntity.query.all()
        assert len(roles) == 1

        # test usage of CRUDMixin.get_by_id() and create()
        role_tech = RoleEntity.save(role_tech)
        assert 2 == role_tech.id

        ordered = RoleEntity.query.order_by(RoleEntity.name).all()
        # verify that we have two rows now
        assert 2 == len(ordered)

        # verify that the attribute is saved
        first = ordered[0]
        assert ROLE_ADMIN == first.name

        # verify that sorting worked
        first = RoleEntity.query.order_by(db.desc(RoleEntity.name)).first()
        assert ROLE_TECHNICIAN == first.name

    def test_user(self):
        """ verify save and find operations """
        added_date = datetime.today()
        access_end_date = utils.get_expiration_date(180)
        user = UserEntity.create(email="admin@example.com",
                                 first="",
                                 last="",
                                 minitial="",
                                 added_at=added_date,
                                 modified_at=added_date,
                                 access_expires_at=access_end_date)
        assert 1 == user.id
        assert "admin@example.com" == user.email

        role_admin = self.get_role(ROLE_ADMIN)
        role_tech = self.get_role(ROLE_TECHNICIAN)
        db.session.add(role_admin)
        db.session.add(role_tech)

        user.roles.append(role_admin)
        user.roles.append(role_tech)

        user_roles = UserRoleEntity.query.all()
        print user_roles
        assert 2 == len(user_roles)

        user_role = UserRoleEntity.get_by_id(1)
        assert 1 == user_role.id

    def test_view_roles(self):
        """ @TODO: add test for viewing users """

        # from flask import url_for
        # response = self.client.post(url_for('/api/list_users'), data={})
        # self.assert_redirects(response, url_for(''))
