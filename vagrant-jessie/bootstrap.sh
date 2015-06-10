#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
SHARED_FOLDER=/vagrant

# import helper functions
. $SHARED_FOLDER/bootstrap_functions.sh

# Exit on first error
set -e

install_utils
install_apache_for_python
#install_nodejs
#install_hello_world
install_dropper
