#!/usr/bin/env bash
#
# Goal: Implement a `one-click` deployment tool
#
# @authors
#   Andrei Sura             <sura.andrei@gmail.com>
#   Taeber Rapczak          <taeber@ufl.edu>


# import helper functions
. deploy_functions.sh

# Exit cleanly on Ctrl-C
trap 'exit 1' INT

# by default we only perform and "update" not a "deploy"
INITIAL_DEPLOY_ONLY=no
SHOW_HELP=no
TAG_NUMBER=""

set -- $(getopt hit: "$@")
while [ $# -gt 0 ]
    do
        case "$1" in
                (-h) SHOW_HELP=yes;;
                (-i) INITIAL_DEPLOY_ONLY=yes;;
                (-t) TAG_NUMBER=$2; shift;;
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
    usage && echo "Incorrect value specified for <target>"
    exit 1
fi

# validate tag number
VALID_TAGS=`git show-ref --tags | grep "refs/tags" | cut -d / -f 3 | paste -sd ' ' -`
VALID_TAGS_ARRAY=( $(git show-ref --tags | grep "refs/tags" | cut -d / -f 3 | paste -sd ' ' -) )

if [[ X"$TAG_NUMBER" = "X" ]]; then
    usage && echo "No deployment tag specified. Please specify a tag to deploy."
    echo "Valid tags list: $VALID_TAGS"
    exit 1
fi

# declare the internal field separator and then check if element is in the array
IFS=:
if ! [[ ":${VALID_TAGS_ARRAY[*]}:" =~ ":$TAG_NUMBER:" ]]; then
    echo "Invalid deployment tag specified: $TAG_NUMBER. Valid tags: $VALID_TAGS"
    unset IFS
    exit 1
else
    echo "Using tag:"
    git show $TAG_NUMBER
fi
unset IFS

eval export HOME=~$(id -un)

# folder for storing a local copy of the code
REPO_PARENT_DIR=$HOME/git
REPO_DIR=$REPO_PARENT_DIR/redi-dropper-client
GIT_REPO=https://github.com/ctsit/redi-dropper-client
VENV_DIR=$HOME/venv
HOST=$1
REPO_URL=`grep "'project_repo'" $HOST/fabric.py | cut -d = -f 2 | tr -d "'"`

test -d "$REPO_PARENT_DIR" || mkdir "$REPO_PARENT_DIR"
test -d "$REPO_DIR" || git clone --single-branch $GIT_REPO $REPO_DIR
pushd $REPO_DIR
    # This is to get a copy of the updated deployment fabfile.py
   git checkout tags/$TAG_NUMBER
popd

check_requirements
activate_venv
install_fabric

# set up PYTHONPATH
export PYTHONPATH=$REPO_DIR:$PYTHONPATH
# CWD to where the fabfile.py is located so we don't have to use 'fab --fabfile'
pushd $REPO_DIR/app/deploy
    fab $HOST print_project_repo

    if [[ "yes" == "$INITIAL_DEPLOY_ONLY" ]]; then
        # create folders, install venv, clone repo from the given branch
        # fab $HOST bootstrap:develop
        fab $HOST bootstrap:$TAG_NUMBER
        fab $HOST enable_site
    else
        fab $HOST deploy:$TAG_NUMBER
    fi

    fab $HOST restart_wsgi_app
    sleep 2
    fab $HOST check_app
popd
