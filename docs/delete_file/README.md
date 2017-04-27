# Edit User README

## Introduction

Welcome to the delete_file feature branch readme

## Changelog

1) Added delete_file api call to support deleteing files from the client if the user 
has the deleter permission
2) Reworked client side to have delete buttons that are enabled when a checkbox is clicked
3) Updated deploy files to apply this upgrade

## Deploying the change

1) Go through standard deploy/upgrade process to get new codebase
2) Run "fab mysql_version_upgrade:4"'
Alternate:
Migrate MySQL to db/004/upgrade.sql via mysql command line (ex. sudo mysql ctsi_dropper_s < db/003/upgrade.sql)

## Smoketest

1) Verify the web application has the deleter permission available on the user admin page
2) Verify that the database contains an entry in table "LogType" with a "logtType" of 
    "file_deleted" and that the "Role" table contains "deleter"

