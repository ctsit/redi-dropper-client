# Helper script for running frequent tasks on the vagrant machine

SHARED_DIR := /vagrant/
VAGR := VAGRANT_CWD=vagrant
VAGR_SSH := $(VAGR) vagrant ssh

help:
	@echo "Available tasks"

	@echo "run                 : run the flask application using the fabric python tool"
	@echo "vup                 : start the testing VM"
	@echo "vas                 : ssh into the testing VM"
	@echo "vdown               : destroy the testing VM (all unsaved files will be lost)"
	@echo "vprov               : re-provision the testing VM"
	@echo "check_apache        : check if Apache is running in the testing VM"


run:
	cd app && fab run

test:
	cd app && fab test

vup:
	$(VAGR) vagrant up

vas:
	$(VAGR_SSH)

vdown:
	$(VAGR) vagrant destroy

vprov:
	$(VAGR) vagrant provision


check_apache:
	@curl -s -k http://localhost | grep 'It works'

clean:
	find . -type f -name "*.pyc" -print | xargs rm -f
