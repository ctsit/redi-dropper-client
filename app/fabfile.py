# -*- coding: utf-8 -*-
"""
The 'fabfile.py' is used by Fabric and must reside in the
application root directory.

@see http://docs.fabfile.org/en/latest/tutorial.html
"""

from __future__ import with_statement
from fabric.api import local, task, prefix, abort
from fabric import colors
from fabric.context_managers import settings
from fabric.contrib.console import confirm
from contextlib import contextmanager

STATUS_PASS = '✔'
STATUS_FAIL = '✗'


@task
def prep_deploy():
    """ Install required Python packages """
    local('pip install -r requirements/deploy.txt')


@task
def prep_develop():
    """ Install required Python packages for developers """
    local('pip install -r requirements/dev.txt')
    local('pip install -r requirements/tests.txt')


def get_db_name():
    with settings(warn_only=True):
        cmd = "grep -i 'create database' db/000/upgrade.sql | cut -d ' ' -f3 " \
            "| tr -d  ';'"
        db_name = local(cmd, capture=True)
    return db_name


def check_db_exists(db_name):
    cmd = "echo 'select count(*) from information_schema.SCHEMATA " \
          "WHERE SCHEMA_NAME = \"{}\"' | mysql -uroot " \
          "| sort | head -1".format(db_name)
    result = local(cmd, capture=True)
    return result


@task
def init_db():
    """ Create the database """
    db_name = get_db_name()
    exists = check_db_exists(db_name)

    if exists:
        abort(colors.red("The database '{}' already exists".format(db_name)))

    if not confirm("Do you want to create the database '{}'?".format(db_name)):
        abort(colors.yellow("Aborting at user request."))

    local('sudo mysql < db/000/upgrade.sql')
    local('sudo mysql ctsi_dropper_s < db/001/upgrade.sql')
    local('sudo mysql ctsi_dropper_s < db/002/upgrade.sql')
    local('sudo mysql ctsi_dropper_s < db/002/data.sql')
    local('sudo mysql ctsi_dropper_s < db/003/upgrade.sql')
    local('sudo mysql ctsi_dropper_s < db/004/upgrade.sql')


@task
def reset_db():
    """ Drop all tables, Create empty tables, and add data. """
    db_name = get_db_name()

    if not confirm("Do you want to erase the '{}' database"
                   " and re-create it?".format(db_name)):
        abort(colors.yellow("Aborting at user request."))

    local('sudo mysql < db/000/downgrade.sql')
    local('sudo mysql < db/000/upgrade.sql')
    local('sudo mysql ctsi_dropper_s < db/001/upgrade.sql')
    local('sudo mysql ctsi_dropper_s < db/002/upgrade.sql')
    local('sudo mysql ctsi_dropper_s < db/002/data.sql')
    local('sudo mysql ctsi_dropper_s < db/003/upgrade.sql')
    local('sudo mysql ctsi_dropper_s < db/004/upgrade.sql')


@task
def test():
    """
    Run the automated test suite using py.test
    """
    local('py.test --tb=short -s tests/')


@task
def coverage():
    """
    Run the automated test suite using py.test

    # https://pytest.org/latest/example/pythoncollection.html
    local('python setup.py nosetests')
    """
    local(
        'py.test --tb=short -s --cov redidropper --cov-config tests/.coveragerc --cov-report term-missing --cov-report html tests/')


@task
def lint():
    local("which pylint || sudo easy_install pylint")
    local("pylint -f parseable redidropper | tee pylint.out")


@task
def run():
    """
    Start the web application using the WSGI webserver provided by Flask
    """
    local('python run.py')


@task
def show_versions(url='https://localhost:5000'):
    """ display latest tag and deployed tag at a specific url
    Example: fab show_versions:url=https://stage.dropper.ctsi.ufl.edu
    """
    local('git fetch --tags')

    cmd = """git tag \
        | sort -t. -k 1,1n -k 2,2n -k 3,3n \
        | tail -1"""
    last_tag = local(cmd, capture=True)

    cmd2 = 'curl -sk {}'.format(url) + """ \
        | grep Version \
        | grep -oE "[0-9.]{1,2}[0-9.]{1,2}[0-9a-z.]{1,4}" \
        | tail -1"""
    deployed_tag = local(cmd2, capture=True)

    print("\nLast tag: {}".format(colors.yellow(last_tag)))
    print("Deployed tag: {}".format(colors.yellow(deployed_tag)))

    if last_tag != deployed_tag:
        print("[{}] Tags do not match!".format(colors.red(STATUS_FAIL)))
    else:
        print("[{}] Tags do match.".format(colors.green(STATUS_PASS)))


@contextmanager
def virtualenv(venv_name):
    """ Activate a context """
    """Usage example:
    def deploy():
        with virtualenv('ha'):
            run("pip freeze > requirements.txt")
    """
    # @see so/questions/1180411/activate-a-virtualenv-via-fabric-as-deploy-user
    with prefix('source ~/.virtualenvs/'+venv_name+'/bin/activate'):
        yield


@task
def clean():
    """
    Remove generated files
    """
    local('rm -rf cover/ htmlcov/ .coverage coverage.xml nosetests.xml')
    local('rm -rf .ropeproject')
    local('find . -type f -name "*.pyc" -print | xargs rm -f')
