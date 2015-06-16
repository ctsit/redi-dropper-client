#!/usr/bin/env python

"""
Goal: Implement wsgi helper for deployment on Apache

@credits https://github.com/translate/pootle/tree/master/deploy

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)

print("Using interpreter: {}".format(sys.version))

# @TODO: Read from the environment or make it a fabric parameter
app_home = '/srv/apps/dropper/src/app/'

# Apache can set the python path for the venv so no need to do it here
# venv_home = '/srv/apps/dropper-alz/app/venv'
# activate_this = os.path.join(venv_home, 'bin/activate_this.py')
# print("Activating venv: {}".format(venv_home))
# execfile(activate_this, dict(__file__=activate_this))

print("Adding application path: {}".format(app_home))
sys.path.insert(0, app_home)

from redidropper.main import app as application, mail
from redidropper import initializer

# Configures routes, models
application = initializer.do_init(application)
mail.init_app(application)
