REDI-Dropper Client
===================

Introduction
------------

This folder is dedicated to storing the code for REDI-Dropper Client Application.

Functional Specifications
-------------------------
https://docs.google.com/document/d/1EQnPwvKQLCYa7ifHXaHCr4lEJK7QcX7VDJOQvEtkbk8/edit

Technical Specifications
------------------------

- Front end: ReacJS - https://facebook.github.io/react/docs/tutorial.html
- Back end: Flask framework - http://flask.pocoo.org/
- Database: 5.6.24-enterprise-commercial-advanced-log MySQL Enterprise Server


Developer's Workflow
--------------------

There are three great tools for python development:

 * virtualenv (allows to isolate python packages required for your application)
 * virtualenvwrapper (allows to switch between virtualenvs)
 * fabric (allows to execute common python tasks in similar way to Makefiles)

@see https://virtualenvwrapper.readthedocs.org/en/latest/

.. raw:: bash

    brew install mysql
    mysql --version
    (mysql  Ver 14.14 Distrib 5.6.24, for osx10.9 (x86_64) using  EditLine wrapper)

    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    sudo pip install fabric

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/git
    source /usr/local/bin/virtualenvwrapper.sh

    mkvirtualenv -p /usr/local/bin/python2.7 redi-dropper-client
    workon redi-dropper-client
    cd ~/git/redi-dropper-client/app
    fab prep_develop
    fab init_db

    # create and edit the settings file
    cp deploy/sample.settings.conf deploy/settings.conf

    # run the application
    fab run
        or
    python run.py

    Finally you can open your browser at https://localhost:5000/ and login as
    admin@example.com with any password


Initial Deployment
------------------

For deployment we use the deploy/deploy.sh shell script.
This script invokes fabric tasks defined in the app/deploy/fabfile.py
aginst the server specified as an argument.

After you clone the repository, execute the following commands to deploy to
staging (or production):

- create three files in your local `deployment` folder:
.. raw:: bash
    $ cp sample.fabric.py staging/fabric.py
    $ cp sample.deploy.settings.conf staging/settings.conf
    $ cp sample.fabric.py staging/fabric.py
- edit the created files to reflect the proper username/passwords/hosts/paths
- execute the initial deployment (requires sudo access on the target server)
.. raw:: bash
    $ deploy/deploy.sh -i staging
    OR
    $ deploy/deploy.sh -i production


Re-Deployment
-------------

Once the application was deployed to the target server we have to re-upload
configuration and code changes by executing one of the following command:

.. raw:: bash
    $ deploy/deploy.sh staging
    OR
    $ deploy/deploy.sh production

Note: that the '-i' flag is used only for the initial deployment.


Files & Folders
---------------

+--------------------+-----------------------------------------------------------------------------+
| **File**           | **Description**                                                             |
+====================+=============================================================================+
| run.py             |  This is the file that is invoked to start up a development server.         |
|                    |  This is not used in production, but it will see a lot of mileage           |
|                    |  in development. In production we use the dropper.wsgi file for Apache.     |
+--------------------+-----------------------------------------------------------------------------+
| requirements/.txt   | This folder stores lists of Python packages that the app depends on.       |
|                    |  We have separate files for production and development dependencies.        |
+--------------------+-----------------------------------------------------------------------------+
| config.py          |  This file contains most of the configuration variables that the app needs. |
+--------------------+-----------------------------------------------------------------------------+
| settings.conf      |  This file contains configuration variables that shouldn't be in version    |
|                    |  control.                                                                   |
|                    |  This includes things like API keys and database URIs containing passwords. |
|                    |  This also contains variables that are specific to this particular instance |
|                    |  of your application.                                                       |
|                    |  For example, you might have                                                |
|                    |      DEBUG = False // in config.py but                                      |
|                    |      DEBUG = True  // in sttings.conf for development.                      |
+--------------------+-----------------------------------------------------------------------------+
| yourapp/           |  This is the package that containsthe bulk of the application code.         |
+--------------------+-----------------------------------------------------------------------------+
| yourapp/routes     |  This is where the routes are defined.                                      |
|                    |  It may be split into a package of its own.                                 |
+--------------------+-----------------------------------------------------------------------------+
| yourapp/models     |  This is where you define the models of your application.                   |
|                    |  This may be split into several modules in the same way as routes.          |
+--------------------+-----------------------------------------------------------------------------+
| yourapp/static/    |  This folder contains the public CSS, JavaScript, images and other files    |
|                    |  that require to be public for the app. It is accessible from               |
|                    |  yourapp.com/static/ by default.                                            |
+--------------------+-----------------------------------------------------------------------------+
| yourapp/templates/ |  This is where we store the Jinja2 templates for the app.                   |
+--------------------+-----------------------------------------------------------------------------+


Debugging
---------

Install http://flask-debugtoolbar.readthedocs.org/en/latest/
The toolbar will automatically be injected into Jinja templates when debug mode is on.
In production, setting app.debug = False will disable the toolbar.


Credits
-------

See `Explore flask page <https://exploreflask.com/organizing.html`__ for more details.
