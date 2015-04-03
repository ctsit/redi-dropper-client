"""
Goal: Store table models

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


# Examples:
# ! http://www.pythoncentral.io/sqlalchemy-orm-examples/
# !! http://www.pythoncentral.io/sqlalchemy-expression-language-advanced/
# !!! http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#self-referential-many-to-many-relationship

# http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
# http://stackoverflow.com/questions/17972020/how-to-execute-raw-sql-in-sqlalchemy-flask-app
# http://www.dangtrinh.com/2013/06/sqlalchemy-python-module-with-mysql.html

# http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/declarative.html
# http://sqlalchemy.readthedocs.org/en/improve_toc/orm/join_conditions.html
# http://stackoverflow.com/questions/16028714/sqlalchemy-type-object-role-user-has-no-attribute-foreign-keys
# https://github.com/mitsuhiko/flask-sqlalchemy/issues/98
# http://version2beta.com/articles/migrating-from-mysql-to-postresql-using-sqlalchemy/


# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers-contacts-and-friends

Base = declarative_base()


class ProjectEntity(Base):
    """ Stores details about projects """
    __tablename__ = 'Project'

    prjID = Column(Integer, primary_key=True)
    prjName = Column(String(255), nullable=False)
    prjUrlHost = Column(String(255), nullable=False)
    prjUrlPath = Column(String(255), nullable=False)
    prjApiKey = Column(String(255), nullable=False)
    prjUrlPath = Column(String(255), nullable=False)
    prjAddedAt = Column(DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    prjModifiedAt = Column(TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')

    __table_args__ = (UniqueConstraint('prjUrlHost', 'prjUrlPath'), )

    def __repr__(self):
        return "<ProjectEntity (prjID: {}, prjName: {}, prjUrlHost: {})>" \
            .format(self.prjID, self.prjName, self.prjUrlHost)


class UserAuthEntity(Base):
    """ Stores the username/password for the user """
    __tablename__ = 'UserAuth'

    uathID = Column(Integer, primary_key=True)
    usrID = Column(Integer, ForeignKey('User.usrID'), nullable=False)
    uathUsername = Column(String(255), nullable=False, unique=True)
    uathPassword = Column(String(255), nullable=False)
    uathPasswordResetToken = Column(String(255), nullable=False, \
            server_default='')
    uathEmailConfirmationToken = Column(String(255), nullable=False, \
            server_default='')
    uathModifiedAt = Column(TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')

    # @OneToOne
    user = relationship('UserEntity', uselist=False)

    def __repr__(self):
        return "<UserAuthEntity (\n\t" \
                "authID: {0}, uathUsername: {1}, uathModifiedAt: {2}, \n\t" \
                "{3}\n)>" \
            .format(self.uathID, self.uathUsername, self.uathModifiedAt, \
                self.user)


class UserEntity(Base):
    """ Stores the basic information about the user """
    __tablename__ = 'User'
    usrID = Column(Integer, primary_key=True)
    usrEmail = Column(String(255), nullable=False, unique=True)
    usrFirst = Column(String(255), nullable=False)
    usrLast = Column(String(255), nullable=False)
    usrMI = Column(String(1), nullable=False)
    usrAddedAt = Column(DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    usrModifiedAt = Column(TIMESTAMP(), nullable=False, \
            server_default='CURRENT_TIMESTAMP')
    usrEmailConfirmedAt = Column(DateTime(), nullable=False, \
            server_default='0000-00-00 00:00:00')
    usrIsActive = Column(Boolean(), nullable=False, server_default='1')

    # @OneToOne
    auth = relationship('UserAuthEntity', uselist=False)

    # @OneToMany
    roles = relationship('RoleEntity', \
            secondary='ProjectUserRole', \
            backref=backref('user'))

    def __init__(self, usrEmail, usrFirst, usrLast, usrMI=''):
        self.usrEmail = usrEmail
        self.usrFirst = usrFirst
        self.usrLast = usrLast
        self.usrMI = usrMI

    def __repr__(self):
        return "<UserEntity (usrID: {}, usrEmail: {})>" \
            .format(self.usrID, self.usrEmail)


class RoleEntity(Base):
    """ Stores possible user roles """
    __tablename__ = 'Role'
    rolID = Column(Integer, primary_key=True)
    rolName = Column(String(255), nullable=False, unique=True)
    rolDescription = Column(String(255), nullable=False)

    # This relationship is not needed for now
    #users = relationship('UserEntity', \
    #    secondary='ProjectUserRole', \
    #    backref=backref('role'))

    def __repr__(self):
        return "<RoleEntity (rolID: {}, rolName: {})>" \
            .format(self.rolID, self.rolName)


class ProjectUserRoleEntity(Base):
    """ Stores the user's project roles """

    __tablename__ = 'ProjectUserRole'
    purID = Column(Integer, primary_key=True)
    prjID = Column(Integer, ForeignKey('Project.prjID', ondelete='CASCADE'), \
            nullable=False)
    usrID = Column(Integer, ForeignKey('User.usrID', ondelete='CASCADE'), \
            nullable=False)
    rolID = Column(Integer, ForeignKey('Role.rolID', ondelete='CASCADE'), \
            nullable=False)

    # @OneToOne
    role = relationship('RoleEntity', uselist=False)
    project = relationship('ProjectEntity', uselist=False)
    user = relationship('UserEntity', uselist=False)

    # Don't allow more than one role for a specific user for a specific project
    __table_args__ = (UniqueConstraint('prjID', 'usrID', name='project_user'), )


    def __repr__(self):
        return "<ProjectUserRoleEntity (\n\t" \
            "purID: {0.purID!r}, \n\t" \
            " {1}, \n\t" \
            " {2}, \n\t" \
            " {3}, \n" \
            ")>".format(self, self.project, self.user, self.role)
