"""
Goal: Init the Flask Singletons 'app' and 'db'
used by ../run.py

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

import time

try:
    from flask import Flask, g
    from flask_sqlalchemy import SQLAlchemy
except ImportError, error:
    import sys
    sys.exit("Missing required package: {}".format(error))


# The WSGI compliant web-application object
app = Flask(__name__)

# The Object-Relationan-Mapping (ORM) object
db = SQLAlchemy(app)



#@app.before_request
#def before_request():
#    """ Set a timer """
#    g.start = time.time()
#

#@app.after_request
#def after_request(response):
#    """
#    @TODO: log how long it took to parse the request
#    """
#    diff = time.time() - g.start
#    app.logger.debug("Exec time: {}".format(str(diff)))
#
#    if response.response and "__EXE_TIME__" in response.response:
#        response.response = response.response.replace(
#            '__EXE_TIME__', str(diff))
#        response.headers["content-length"] = len(response.response)
#
#    return response

#@app.teardown_request
#def end_of_request(exception=None):
#    """ Release resources """
#    if exception is not None:
#        app.logger.debug("end_of_request() exception: {}".format(exception))
#
#    if app.db_session is not None:
#        #app.logger.debug("removing session...")
#        app.db_session.remove()
