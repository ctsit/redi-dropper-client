#!/usr/bin/env bash
#
# Goal: implement helper functions used by manage.sh
#
# @authors:
#  Andrei Sura <sura.andrei@gmail.com>

MSG_INSTALL="Please install it first"

function usage() {
    echo "Usage: "
    echo "   $0 [-i initial deployment] [-h help] [-t tag_number] target <staging|production>"
}

function get_md5_exe() {
    OS=`uname -s`
    # brew install md5sha1sum
    if [ "Darwin" == $OS ]; then
        echo "md5 -r"
    elif [ "Linux" == $OS ]; then
        echo "md5sum"
    else
        echo "Unsupported os: $OS"
        exit 1
    fi
}

function check_requirements() {
    echo "Using REPO_DIR: $REPO_DIR"
    echo "Using VENV_DIR: $VENV_DIR"
    echo "Using REPO_URL: $REPO_URL"
    OS=`uname -s`

    if [ "Darwin" == $OS ]; then
        check_requirements_darwin
    elif [ "Linux" == $OS ]; then
        check_requirements_linux
    else
        echo "Unsupported os: $OS"
        exit 1
    fi
}

function has_required() {
    REQ=$1
    MSG="Missing requirement: $REQ"

    if test -z `which $REQ`; then
        echo $MSG
        return 1
    fi
    return 0
}

function check_requirements_darwin() {
    # if no python, check brew, ruby, curl
    if ! has_required 'python'; then
        if ! has_required 'brew'; then
            if ! has_required 'ruby'; then
                echo $MSG_INSTALL && exit 1
            fi
            if ! has_required 'curl'; then
                echo $MSG_INSTALL && exit 1
            fi
            ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        else
            # also installs pip...
            brew install python
            sudo pip install --upgrade pip
            sudo pip install --upgrade virtualenv
        fi
    else
        python --version
    fi

    if ! has_required 'pip'; then
        echo $MSG_INSTALL && exit 1
    fi
    if ! has_required 'virtualenv'; then
        sudo pip install virtualenv
    fi
}

function check_requirements_linux() {
    # if no python, check brew, ruby, curl
    if ! has_required 'python'; then
        apt-get install python-dev python-pip build-essential
        sudo pip install --upgrade pip
        sudo pip install --upgrade virtualenv
    fi
    python --version

    if ! has_required 'pip'; then
        echo $MSG_INSTALL && exit 1
    fi
    if ! has_required 'virtualenv'; then
        sudo pip install --upgrade virtualenv
    fi
}

function activate_venv() {
    if test -d $VENV_DIR; then
        echo "Venv folder: [$VENV_DIR] already exists."
        read -p "Do you want to continue? [y/N] " -n 1 -r

        echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        virtualenv $VENV_DIR
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
