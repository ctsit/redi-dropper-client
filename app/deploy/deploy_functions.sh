#!/usr/bin/env bash
#
# Goal: implement helper functions used by manage.sh
#
# @authors:
#  Andrei Sura <sura.andrei@gmail.com>

function usage() {
    echo "Usage: "
    echo "   $0 [-i initialize only] [-h help] target <staging|production>"
}

# function parse_args() {}

function check_requirements() {
    # @TODO: check for python, pip, virtualenv
    test ! -z `which virtualenv` || sudo pip install virtualenv
}

function activate_venv() {
    if [ -d $VENV_DIR ]; then
        echo "Venv folder: [$VENV_DIR] already exists."
        read -p "Do you want to continue? [y/N] " -n 1 -r

        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Executing: $3"
            `$3`
        else
            exit 1
        fi
    fi
    . $VENV_DIR/bin/activate
}

function install_fabric() {
    # exec after the virtualenv is activated
    type fab >/dev/null 2>&1 || {
        echo >&2 "fabric is not installed.";
        pip install fabric
    }
}

function execute_fresh_script() {
    echo "Checking if repo was updated..."
    SUM_NEW="$(md5sum $0 | cut -d ' ' -f1):$(md5sum deploy_functions.sh | cut -d ' ' -f1)"
    echo "Compare checksums: $1 vs $SUM_NEW"

    if (cd $REPO_DIR && git pull && git checkout develop); then
        if [ "$SUM" != "$SUM_NEW" ]; then
            echo "Re-executing updated script"
            exec $0 "$@"
        fi
    fi
}
