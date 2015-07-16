#!/usr/bin/env bash

# import helper functions
. deploy_functions.sh

# Exit cleanly on Ctrl-C
trap 'exit 1' INT

# by default we only perform and "update" not a "deploy"
INITIAL_DEPLOY_ONLY=no
SHOW_HELP=no

set -- $(getopt ih "$@")
while [ $# -gt 0 ]
    do
case "$1" in
        (-i) INITIAL_DEPLOY_ONLY=yes;;
        (-h) SHOW_HELP=yes;;
        (--) shift; break;;
        (-*) echo "$0: error - unrecognized option $1" 1>&2; exit 1;;
        (*)  break;;
        esac
        shift
done

if [[ $# -lt 1 ]] || [[ "yes" == "$SHOW_HELP" ]] ; then
    usage
    exit 1
fi

if ! [[ X"$1" = Xstaging ]] && ! [[ X"$1" = Xproduction ]]; then
    usage
    echo "Incorrect value specified for <target>"
    exit 1
fi

eval export HOME=~$(id -un)

# folder for storing a local copy of the code
REPO_PARENT_DIR=$HOME/git
REPO_DIR=$REPO_PARENT_DIR/redi-dropper-client
GIT_REPO=https://github.com/ctsit/redi-dropper-client
VENV_DIR=$HOME/venv
HOST=$1

test -d "$REPO_PARENT_DIR" || mkdir "$REPO_PARENT_DIR"
test -d "$REPO_DIR" || git clone $GIT_REPO $REPO_DIR
pushd $REPO_DIR
    # @TODO: use a tag number instead of develop branch
    git pull && git checkout develop
popd

check_requirements
activate_venv
install_fabric

# set up PYTHONPATH
export PYTHONPATH=$REPO_DIR:$PYTHONPATH
# CWD to where the fabfile.py is located so we don't have to use 'fab --fabfile'
pushd $REPO_DIR/app/deploy
    if [[ "yes" == "$INITIAL_DEPLOY_ONLY" ]]; then
        # create folders, install venv, clone repo from the given branch
        fab $HOST bootstrap_develop
    fi

    # re-check code an requirements (assumes that bootstrap was performed)
    fab $HOST print_project_repo
    fab $HOST disable_site
    # @TODO: use a tag number instead of develop branch
    fab $HOST deploy:develop
    fab $HOST restart_wsgi_app
    sleep 2
    fab $HOST check_app

    # show error log from the remote server
    #fab staging show_config_apache
    #fab staging show_errors_apache
popd
