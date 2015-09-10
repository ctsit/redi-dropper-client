#!/bin/bash

function configure_base() {
   # Use local time so we don't have to do math when looking thru logs
   echo "US/Eastern" > /etc/timezone
   dpkg-reconfigure tzdata

   # Update packages
   apt-get update -y
   #apt-get upgrade -y
}

function install_utils() {
   cp $SHARED_FOLDER/dot_files/aliases /home/vagrant/.bash_aliases
   cp $SHARED_FOLDER/dot_files/aliases /root/.bash_aliases

   cp $SHARED_FOLDER/dot_files/vimrc /home/vagrant/.vimrc
   cp $SHARED_FOLDER/dot_files/vimrc /root/.vimrc

   cp $SHARED_FOLDER/dot_files/sqliterc /home/vagrant/.sqliterc
   cp $SHARED_FOLDER/dot_files/sqliterc /root/.sqliterc

   apt-get install -y vim ack-grep
}

function install_redis() {

}

function install_openvas() {

}

function install_apache_for_python() {
   # https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
   apt-get install -y \
      apache2 libapache2-mod-wsgi \
      python-dev python-pip \
      mysql-server libmysqlclient-dev \
      libffi-dev \
      libsqlite3-dev
}

function install_dropper() {
    # The vagrant uses the dedicated startup script ==> vagrant.wsgi
    # in order to avoid changing the default ==> dropper.wsgi
    #
    # Note: Apache is configured to set the python-path
    #   ==> /var/www/dropper/venv/lib/python2.7/site-packages

    pushd /var/www/dropper
        # Setting up a virtual environment will keep the application and its
        # dependencies isolated from the main system.

        log "Install via pip: virtualenv..."
        pip install virtualenv
        log "Creating virtual environment: /var/www/app/venv"
        virtualenv venv
        . venv/bin/activate
            log "Installing required python packages..."
            pip install -r app/requirements/dev.txt
        deactivate
    popd

    pushd /var/www/dropper/app/deploy
        log "Link app config file"
        ln -sfv sample.settings.conf settings.conf
    popd

    pushd /var/www/dropper/app
        log "Creating database and tables..."

        if [ -d /var/lib/mysql/$DB_NAME ]; then
            log "Database $DB_NAME already exists... removing"
            mysql < db/000/downgrade.sql
        fi

        log "Execute sql: db/000/upgrade.sql"
        mysql < db/000/upgrade.sql
        log "Execute sql: db/001/upgrade.sql"
        mysql ctsi_dropper_s   < db/001/upgrade.sql
        log "Execute sql: db/002/upgrade.sql"
        mysql ctsi_dropper_s   < db/002/upgrade.sql
        log "Execute sql: db/002/data.sql"
        mysql ctsi_dropper_s   < db/002/data.sql

        log "Stop apache in order to disable the default site"
        service apache2 stop
        a2dissite 000-default

        log "Link config files for apache port 80 and 443"
        ln -sfv /vagrant/apache.conf /etc/apache2/sites-available/dropper.conf
        ln -sfv /vagrant/apache-ssl.conf /etc/apache2/sites-available/dropper-ssl.conf
        ln -sfv /vagrant/apache.conf /etc/apache2/sites-enabled/dropper.conf
        ln -sfv /vagrant/apache-ssl.conf /etc/apache2/sites-enabled/dropper-ssl.conf

        log "Enable apache modules: ssl, headers"
        a2enmod ssl
        a2enmod headers

        log "Restaring Apache with new config..."
        sleep 2
        service apache2 start

        log "Activate the python wsgi app"
        touch -af /var/www/dropper/app/deploy/vagrant.wsgi
        curl -sk https://localhost | grep -i 'what is'
    popd
}


function log() {
    echo -n "Log: "
    echo $*
}
