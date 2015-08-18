#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
SHARED_FOLDER=/vagrant
DB_NAME=ctsi_dropper_s
DB_USER=ctsi_dropper_s

# import helper functions
. $SHARED_FOLDER/bootstrap_functions.sh

# Exit on first error
set -e

configure_base
install_utils
install_apache_for_python
install_dropper
