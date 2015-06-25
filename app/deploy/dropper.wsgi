#!/usr/bin/env python

"""
Goal: Implement wsgi helper for deployment on Apache

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
print("Adding application path: {}".format(app_home))
sys.path.insert(0, app_home)

from redidropper.main import app as application, mail
from redidropper import initializer
from config import MODE_PROD

# Configures routes, models
application = initializer.do_init(application)
mail.init_app(application)
