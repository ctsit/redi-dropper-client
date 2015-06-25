#!/bin/bash

function install_apache_for_python() {
   # https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
    apt-get install -y \
        apache2 \
        libapache2-mod-wsgi \
        libapache2-mod-uwsgi

    apt-get install -y \
        mysql-client \
        libmysqlclient-dev \
        mysql-server \

    apt-get install -y \
        python-dev \
        python-setuptools \
        python-mysqldb \
        python-pip \
        libffi-dev \
        libsqlite3-dev \
        libssl-dev

    # Setting up a virtual environment will keep the application and its dependencies isolated from the main system.
    # Changes to it will not affect the cloud server's system configurations.
    pip install virtualenv virtualenvwrapper fabric

    # service mysql restart
    # service apache2 restart
    # apachectl configtest
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

function install_hello_world() {
    echo "Running install_hello_world()"

    pushd /var/www/app
    virtualenv venv
    source venv/bin/activate
    pip install Flask

    # Run the demo app
    python /home/vagrant/hello.py &
    sleep 2
    curl -s http://localhost:5000
    echo "Done."
    popd
}

function install_dropper() {
    echo "Running install_dropper()"

    pushd /var/www/app
    virtualenv venv
    source venv/bin/activate
    # fab install_requirements
    pip install -r requirements.txt

    # Create the config file
    cp ./deploy/sample.settings.conf ./deploy/settings.conf

    # Start the app manually
    python run.py --port 443 &
    sleep 2
    # curl -skL https://localhost/api
    echo "ssh vagrant@192.168.50.100 or open https://localhost "
    popd
}
