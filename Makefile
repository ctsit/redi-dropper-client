# Helper script for running frequent tasks on the vagrant machine

SHARED_DIR := /vagrant/
VAGR := VAGRANT_CWD=vagrant
VAGR_SSH := $(VAGR) vagrant ssh

help:
	@echo ""
	@echo "Available tasks:"
	@echo "\t run                 : run the flask application using the fabric python tool"
	@echo "\t test                : run pytests"
	@echo "\t vup                 : start the testing VM"
	@echo "\t vas                 : ssh into the testing VM"
	@echo "\t vdown               : destroy the testing VM (all unsaved files will be lost)"
	@echo "\t vprov               : re-provision the testing VM"
	@echo "\t check_apache        : check if Apache is running in the testing VM"
	@echo ""

run:
	cd app && fab run

test:
	cd app && fab test_cov

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
	rm -f app/.coverage app/pylint.out
	rm -rf app/htmlcov/
