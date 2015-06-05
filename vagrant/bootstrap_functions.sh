#!/bin/bash

function configure_base() {
   # Use local time so we don't have to do math when looking thru logs
   echo "US/Eastern" > /etc/timezone
   dpkg-reconfigure tzdata

   # Update packages
   apt-get update -y
   apt-get upgrade -y
}

function install_apache_for_python() {
   # https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
   apt-get install -y \
      apache2 libapache2-mod-wsgi \
      python-dev python-pip \
      mysql-server libmysqlclient-dev \
      libffi-dev \
      libsqlite3-dev

   # Setting up a virtual environment will keep the application and its dependencies isolated from the main system.
   # Changes to it will not affect the cloud server's system configurations.
   pip install virtualenv
}

function install_dropper() {
   pushd /var/www/app

      sed -i'.bak' 's#/srv/apps/dropper-alz#/var/www#' ./deploy/dropper.wsgi

      virtualenv venv
      source venv/bin/activate
         pip install fabric
         fab install_requirements
         #fab init_db
         mysql < db/001/upgrade.sql
         mysql < db/002/upgrade.sql
         mysql < db/002/data.sql
      deactivate

      # Copy most of the sample settings, but change the DB user and password
      cat ./deploy/sample.settings.conf | grep -v DB_USER | grep -v DB_PASS \
         > ./deploy/settings.conf
      echo "DB_USER = 'root'" >> ./deploy/settings.conf
      echo "DB_PASS = ''" >> ./deploy/settings.conf

      service apache2 stop
      a2dissite 000-default
      ln -s /vagrant/apache.conf /etc/apache2/sites-available/dropper.conf
      ln -s /vagrant/apache-ssl.conf /etc/apache2/sites-available/dropper-ssl.conf
      ln -s /vagrant/apache.conf /etc/apache2/sites-enabled/dropper.conf
      ln -s /vagrant/apache-ssl.conf /etc/apache2/sites-enabled/dropper-ssl.conf
      a2enmod ssl
      service apache2 start

   popd
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

