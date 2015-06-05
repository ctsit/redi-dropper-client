#!/bin/bash

function install_apache_for_python() {
   # https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
    apt-get update
    apt-get install -y \
        mysql-client \
        libmysqlclient-dev \
        mysql-server \
        apache2 \
        libapache2-mod-wsgi \
        libapache2-mod-uwsgi \
        python-dev \
        python-setuptools \
        python-mysqldb \
        python-pip

    # Setting up a virtual environment will keep the application and its dependencies isolated from the main system.
    # Changes to it will not affect the cloud server's system configurations.
    pip install virtualenv virtualenvwrapper fabric

    service mysql restart
    a2enmod wsgi
    a2enmod uwsgi

    service apache2 restart
    apachectl configtest
}

function install_nodejs() {
   # https://www.digitalocean.com/community/tutorials/how-to-install-express-a-node-js-framework-and-set-up-socket-io-on-a-vps

   curl -sL https://deb.nodesource.com/setup | bash -
   apt-get install -y nodejs

   # To compile and install native addons from npm you may also need to install build tools:
   apt-get install -y build-essential

   npm install npm -g
   npm install -g express
}

function install_utils() {
   cp $SHARED_FOLDER/aliases /home/vagrant/.bash_aliases
   cp $SHARED_FOLDER/aliases /root/.bash_aliases
   cp $SHARED_FOLDER/vimrc /home/vagrant/.vimrc
   cp $SHARED_FOLDER/vimrc /root/.vimrc
   apt-get install -y \
      vim vim-runtime \
      ctags vim-doc vim-scripts \
      ack-grep \
      git \
      curl \
      nmap \
      tree \
      locate
}

function install_demo_app_old() {
    echo "Running install_demo_app()"

    pushd /var/www/app
    virtualenv venv
    source venv/bin/activate
    pip install fabric
    fab install_requirements

    # Run the demo app
    python hello.py &
    sleep 2
    curl -s http://localhost:5000
    echo "Done."
    popd
}

function install_demo_app() {
    echo "Running install_demo_app()"

    pushd /var/www/app
    virtualenv venv
    source venv/bin/activate
    pip install fabric
    fab install_requirements

    # Run the demo app
    python run.py &
    sleep 2
    curl -skL https://localhost:5000/api
    echo "ssh vagrant@192.168.50.100  or open https://localhost:5002 "
    popd
}
