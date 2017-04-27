# Application README

## Introduction

Welcome to the REDIDropper web application.


## Developer's Workflow - With Vagrant

Steps:

    $ git clone git@github.com:ctsit/redi-dropper-client.git
    $ cd redi-dropper-client/vagrant
    $ vagrant up
    $ open the browser at https://localhost:7088/ (accept the "Your connection is not private" message)

Optional step - create a self-signed certificate:

    $ cd redi-dropper-client/app/ssl
    $ ./gen_cert.sh

The above command will produce two files used in debug mode:

- server.crt
- server.key

Note: if you get errors related to mising "Guest Additions" please try:

    vagrant plugin install vagrant-vbguest

If you get errors related to Unknown configuration section 'trigger', please try:

    vagrant plugin install vagrant-triggers

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

For code deployment we use the **app/deploy/deploy.sh** shell script.
This script invokes fabric tasks defined in the **app/deploy/fabfile.py**
against the "staging" or "production" server specified as an argument.

Steps:

- Clone the repository
- Refresh the list of tags from the repository:

    $ git fetch --tags

- Create the required files in your local **deploy** folder:

        $ cd redi-dropper-client/app/deploy
        $ cp sample.fabric.py               staging/fabric.py
        $ cp sample.deploy.settings.conf    staging/settings.conf
        $ cp sample.virtualhost.conf        staging/virtualhost.conf
        $ cp sample.virtualhost-ssl.conf    staging/virtualhost-ssl.conf

- Edit the files in the staging (or production) folder to reflect
  the proper username/passwords/hosts/paths.
  This is the list of variables that need to be changed:

<pre>
 1.   SETTINGS['hosts'] = ['PLEASE_EDIT_ME']  # ['dropper1.ctsi.ufl.edu']
 2.   SETTINGS['user'] = 'PLEASE_EDIT_ME'  # 'the_deployer'
 3.   SETTINGS['db_user'] = 'PLEASE_EDIT_ME'
 4.   SETTINGS['db_pass'] = 'PLEASE_EDIT_ME'
 5.   SETTINGS['db_host'] = 'PLEASE_EDIT_ME'
 6.   SETTINGS['db_name'] = 'PLEASE_EDIT_ME'
 7.   SETTINGS['redidropper_upload_temp_dir'] = 'PLEASE_EDIT_ME'  # '/ext/www/prod/mri_images_temp'
 8.   SETTINGS['redidropper_upload_saved_dir'] = 'PLEASE_EDIT_ME'  # '/ext/www/prod/mri_images'
 9.   SETTINGS['redcap_api_token'] = 'PLEASE_EDIT_ME'  # 'the secret'
 10.  SETTINGS['redcap_demographics_subject_id'] = 'PLEASE_EDIT_ME'  # 'ptid'
 11.  SETTINGS['project_name'] = 'PLEASE_EDIT_ME'  # 'dropper'
 12.  SETTINGS['project_url'] = 'PLEASE_EDIT_ME'  # 'dropper.ctsi.ufl.edu'
 13.  SETTINGS['server_user'] = 'PLEASE_EDIT_ME'  # 'www-data'
 14.  SETTINGS['server_group'] = 'PLEASE_EDIT_ME'  # 'www-data'
</pre>

  Note: an easier option would be to ask another developer to provide these
  files to you.

- Execute the **initial deploy** (using `-i` option) command for staging (or production):

        $ cd redi-dropper-client/app/deploy
        $ git fetch --tags
        $ ./deploy.sh -i -t tag_number -r ~/git staging
        OR
        $ ./deploy/deploy.sh -i -t tag_number -r ~/git production

Once you have the fabric tool installed you can create the database tables
in staging or production databases:

    $ fab staging mysql_conf
    $ fab staging mysql_list_tables
    $ fab staging mysql_create_tables

If tables already exist in the database and you wish to **re-create** them
please run:

    $ fab staging mysql_reset_tables

Note: Reseting tables does not create a backup of the tables so please
**make sure** the existing data can be discarded.


## Re-Deployment

This is the process through which the developers will commonly deploy
fixes and improvements **after** an instance was deployed to production.

Steps:

- Create and update the configuration files to reflect the latest settings
(see the "Initial Deployment")
- Refresh the list of tags from the repository:

    $ git fetch --tags

- Re-upload configuration and code changes by executing one of the following:

    $ deploy/deploy.sh -t `tag_number` -r ~/git staging

    OR

    $ deploy/deploy.sh -t `tag_number` -r ~/git  production

<div style="border: solid 1px red; padding: 2em; font-weigh: bold">
Warning: **Do not use** the <b>-i</b> flag since it is intended only for the
        initial deployment.
</div>

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


# Functional Specifications

@TODO: import from Forge wiki


# Technical Specifications

- Front end: [ReacJS](https://facebook.github.io/react/docs/tutorial.html)
- Back end: [Flask framework](http://flask.pocoo.org)
- Database: [MySQL Enterprise Server v5.6.24](http://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-24.html)


## Credits

See [Explore flask page](<https://exploreflask.com/organizing.html)
