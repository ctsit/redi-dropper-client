#!/usr/bin/env python

"""
Goal: Implement wsgi helper for deployment on Apache

@credits https://github.com/translate/pootle/tree/master/deploy

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
"""

import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)

# @TODO: Read from the environment
app_home = '/srv/apps/dropper-alz/app/'
venv_home = '/srv/apps/dropper-alz/app/venv'

print("Using interpreter: {}".format(sys.version))

activate_this = os.path.join(venv_home, 'bin/activate_this.py')
print("Activating venv: {}".format(venv_home))
execfile(activate_this, dict(__file__=activate_this))

print("Adding application path: {}".format(app_home))
sys.path.insert(0, app_home)

from redidropper.main import app as application, mail
from redidropper.startup import initializer

# Configures routes, models
application = initializer.do_init(application)
mail.init_app(application)

# print application.url_map
# dir = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    """ Entry point for command line execution """
    ssl_context = initializer.get_ssl_context(app)
    #app.run(ssl_context=ssl_context)
    app.run()
