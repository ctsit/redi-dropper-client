#!/bin/bash

function install_apache_for_python() {
   # https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
	apt-get update
	apt-get install -y \
		apache2 \
      libapache2-mod-wsgi \
      python-dev \
      python-setuptools \
      python-pip

   # Setting up a virtual environment will keep the application and its dependencies isolated from the main system.
   # Changes to it will not affect the cloud server's system configurations.
   pip install virtualenv

	service apache2 restart
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
      tree
}


function install_demos() {
   # Edit /etc/apache2/sites-available/FlaskApp.conf

   pushd /var/www/app

   virtualenv venv
   source venv/bin/activate
   pip install Flask
   pip install flask-debugtoolbar
   # Successfully installed Flask-0.10.1 Jinja2-2.7.3 Werkzeug-0.10.1 itsdangerous-0.24 markupsafe-0.23

   # Run the demo app
   python redidropper/__init__.py &
   curl -s http://127.0.0.1:5000/ | grep 'Hello World'
   popd
}
