# Application README

## Introduction

This folder stores the code for RediDropper web application.


# Functional Specifications

@TODO: import from Forge wiki


# Technical Specifications

- Front end: [ReacJS](https://facebook.github.io/react/docs/tutorial.html)
- Back end: [Flask framework](http://flask.pocoo.org)
- Database: [MySQL Enterprise Server v5.6.24](http://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-24.html)


## Developer's Workflow - With Vagrant

* git clone git@github.com:ctsit/redi-dropper-client.git
* cd redi-dropper-client/vagrant
* vagrant up
* open the browser at https://localhost:7088/ (accept the "Your connection is not private" message)

Optional step - create a self-signed certificate:

    $ cd redi-dropper-client/app/ssl
    $ ./gen_cert.sh

The above command will produce two files used in debug mode:

- server.crt
- server.key

Note: if you get errors related to mising "Guest Additions" please try:

    vagrant plugin install vagrant-vbguest

## Developer's Workflow - Without Vagrant

There are three great tools for python development:

 * [virtualenv](https://virtualenv.pypa.io/en/latest/)
    --> allows to isolate python packages required for your application
 * [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
    --> allows to switch between virtualenvs
 * [fabric](https://fabric.readthedocs.org/en/latest/)
    --> allows to execute common python tasks in similar way to Makefiles


Developers have the option of using the vagrant or run the application
manually using Python's embedded webserver.

The manual process requires the following commands for setup:

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

    # create and edit the settings file to make it visible in config.py
    cp deploy/sample.vagrant.settings.conf deploy/settings.conf

    # run the application
    fab run
        or
    python run.py

    Finally you can open your browser at https://localhost:5000/ and login as
    admin@example.com with any password


# Initial Deployment

Assumptions:
 - The 'deployer' has an account on the target server and it is in the
    `sudoers` group
 - The 'deployer' uses a Darwin/Linux operating system to run the
    deployment script

For code deployment we use the app/deploy/deploy.sh shell script.
This script invokes fabric tasks defined in the app/deploy/fabfile.py
aginst the "staging" or "production" server specified as an argument.

After you clone the repository:

- create the required files in your local `deploy` folder:

    $ cd redi-dropper-client/app/deploy
    $ cp sample.fabric.py               staging/fabric.py
    $ cp sample.deploy.settings.conf    staging/settings.conf
    $ cp sample.virtualhost.conf        staging/virtualhost.conf
    $ cp sample.virtualhost-ssl.conf    staging/virtualhost-ssl.conf

- edit the files in the staging (or production) folder to reflect
  the proper username/passwords/hosts/paths
  Note: an easier option would be to ask another developer to provide these
  files to you.

- execute the initial deploy' command for staging (or production):

    $ cd redi-dropper-client/app/deploy
    $ git fetch --tags upstream
    $ ./deploy.sh -i -t tag_number -r ~/git staging
    OR
    $ ./deploy/deploy.sh -i -t tag_number -r ~/git production

Once you have the fabric tool installed you can create the database tables
in staging or production databases:

    $ fab staging mysql_conf
    $ fab staging mysql_list_tables
    $ fab staging mysql_create_tables

If tables already exist in the database and you wish to re-create them
please run:

    $ fab staging mysql_reset_tables

Note: Reseting tables does not create a backup of the tables so please
make sure the existing data can be discarded.


## Re-Deployment

This is the process through which the developers will commonly deploy
fixes and improvements **after** an instance was deployed to production.

Assumptions:
 - See the "Initial Deployment" assumptions

Re-upload configuration and code changes by executing one of the following:

    $ deploy/deploy.sh -t tag_number -r ~/git staging
    OR
    $ deploy/deploy.sh -t tag_number -r ~/git  production

Note: You might need to refresh the list of tags from the upstream

<pre>
$ git fetch --tags upstream
</pre>

Warning: **Do not use** the `-i` flag since it is intended only for the
        initial deployment.


## Files & Folders

<pre>
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
</pre>


## Debugging

Install http://flask-debugtoolbar.readthedocs.org/en/latest/
The toolbar will automatically be injected into Jinja templates when debug mode is on.
In production, setting app.debug = False will disable the toolbar.


## Credits

See [Explore flask page](<https://exploreflask.com/organizing.html)
