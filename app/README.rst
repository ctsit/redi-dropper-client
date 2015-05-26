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
@TODO:


Workflow
--------

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
    fab install_requirements
    fab init_db

    # create/update important configuration params
    cp redidropper/application.conf.sample ~/redidropper_application.conf

    # run the application
    REDIDROPPER_CONFIG=~/redidropper_application.conf python run.py

    # to avoid typing the REDIDROPPER_CONFIG=... you can create a permanent
    # environment entry in your ~/.bashrc
    echo 'export REDIDROPPER_CONFIG=~/redidropper_application.conf' >> ~/.bashrc && . ~/.bashrc
    # ... and then you can simply run
    ./run.sh
        or
    python run.py
	or
    fab run

    Finally you can opn your browser at https://localhost:5000/ and login as 
    admin@example.com with any password

Files & Folders
---------------

+--------------------+-----------------------------------------------------------------------------+
| **File**           | **Description**                                                             |
+====================+=============================================================================+
| run.py             |  This is the file that is invoked to start up a development server.         |
|                    |  It gets a copy of the app from your package and runs it.                   |
|                    |  This won't be used in production, but it will see a lot of mileage         |
|                    |  in development.                                                            |
+--------------------+-----------------------------------------------------------------------------+
| requirements.txt   |  This file lists all of the Python packages that your app depends on.       |
|                    |  You may have separate files for production and development dependencies.   |
+--------------------+-----------------------------------------------------------------------------+
| config.py          |  This file contains most of the configuration variables that your app needs.|
+--------------------+-----------------------------------------------------------------------------+
| application.cfg    |  This file contains configuration variables that shouldn't be in version    |
|                    |  control.                                                                   |
|                    |  This includes things like API keys and database URIs containing passwords. |
|                    |  This also contains variables that are specific to this particular instance |
|                    |  of your application.                                                       |
|                    |  For example, you might have                                                |
|                    |      DEBUG = False // in config.py but                                      |
|                    |      DEBUG = True  // in application.cfg for development.                   |
|                    |  Since this file will be read in after config.py, it will override it and   |
|                    |  set DEBUG = True.                                                          |
+--------------------+-----------------------------------------------------------------------------+
| yourapp/           |  This is the package that contains your application.                        |
+--------------------+-----------------------------------------------------------------------------+
| yourapp/__init__.py|  This file initializes your application and brings together all of          |
|                    |  the various components.                                                    |
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
| yourapp/templates/ |   This is where you'll put the Jinja2 templates for your app.               |
+--------------------+-----------------------------------------------------------------------------+


Debugging
---------

Install http://flask-debugtoolbar.readthedocs.org/en/latest/

.. code:: python

    from flask import Flask
    from flask_debugtoolbar import DebugToolbarExtension
    app = Flask(__name__)

    # the toolbar is only enabled in debug mode:
    app.debug = True
    # set a 'SECRET_KEY' to enable the Flask session cookies
    app.config['SECRET_KEY'] = '<replace with a secret key>'
    toolbar = DebugToolbarExtension(app)


The toolbar will automatically be injected into Jinja templates when debug mode is on.
In production, setting app.debug = False will disable the toolbar.


Credits
-------

See `Explore flask page <https://exploreflask.com/organizing.html`__ for more details.
