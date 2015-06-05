#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
SHARED_FOLDER=/vagrant

# import helper functions
. $SHARED_FOLDER/bootstrap_functions.sh

install_utils
install_apache_for_python
install_demo_app
#install_nodejs
