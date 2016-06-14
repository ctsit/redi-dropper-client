# Edit User README

## Introduction

Welcome to the edit_user feature branch readme

## Changelog

1) Added edit_user api call to support changing users in the web application
2) Reworked client side to use checkboxes and corrected middle name to middle initial
3) Added API unit tests for save_user and edit_user
4) Added functions to deploy/fabfile to support upgrading and downgrading the database

## Deploying the change

1) Go through standard deploy/upgrade process to get new codebase
2) Run "fab mysql_version_upgrade:3"'
Alt2) Migrate MySQL to db/003/upgrade.sql via mysql command line

## Smoketest

1) Verify the web application has checkboxes in the add user form on the admin page
2) Verify that the database contains an entry in table "LogType" with a "logtType" of 
    "account_updated"

