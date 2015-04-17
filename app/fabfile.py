"""
The 'fabfile.py' is used by Fabric and must reside in the
application root directory.

@see http://docs.fabfile.org/en/latest/tutorial.html

@TODO add deploy task
http://flask.pocoo.org/docs/0.10/patterns/fabric/#fabric-deployment
"""

from __future__ import with_statement
from fabric.api import local, task, prefix, abort
from fabric.contrib.console import confirm
from contextlib import contextmanager

@task
def tasks():
    """
    List available tasks
    """
    local("fab --list")

@task
def install_requirements():
    """
    Install required Python packages using: pip install -r requirements.txt
    """
    local('pip install -r requirements.txt')


@task
def reset_db():
    """
    Drop all tables, Create empty tables, and populate tables

    sudo mysql < db/001/downgrade.sql && sudo mysql < db/001/upgrade.sql
    sudo mysql < db/002/downgrade.sql && sudo mysql < db/002/upgrade.sql \
            && sudo mysql < db/002/data.sql
    """
    if not confirm("Do you want to drop all tables and start from scratch?"):
        abort("Aborting at user request.")
    #local('PYTHONPATH=. python redidropper/startup/db_manager.py')
    local('sudo mysql < db/001/downgrade.sql && sudo mysql < db/001/upgrade.sql')
    local('sudo mysql < db/002/downgrade.sql && sudo mysql < db/002/upgrade.sql')
    local('sudo mysql < db/002/data.sql')

@task
def test():
    """
    Run the automated test suite using py.test
    """
    local('py.test --tb=short -s tests/')

@task
def test_cov():
    """ Alias for coverage"""
    coverage()

@task
def cov():
    """ Alias for coverage"""
    coverage()

@task
def coverage():
    """
    Run the automated test suite using py.test

    # https://pytest.org/latest/example/pythoncollection.html
    local('python setup.py nosetests')
    """
    local("""
    py.test \
        --tb=short -s \
        --cov redidropper \
        --cov-config tests/.coveragerc \
        --cov-report term-missing \
        --cov-report html \
        tests/""")

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
def deploy():
    """
    Deploy web application to Heroku.
    Requires: heroku git:remote -a PROJECTNAME
    """
    local('git push heroku master')


@contextmanager
def virtualenv(venv_name):
    """ Activate a context """
    with prefix('source ~/.virtualenvs/'+venv_name+'/bin/activate'):
        yield

@task
def clean():
    """
    Remove generated files
    """
    local('rm -rf cover/ htmlcov/ .coverage coverage.xml nosetests.xml')
    local('find . -type f -name "*.pyc" -print | xargs rm -f')
