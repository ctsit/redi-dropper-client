"""
Goal: Init the Flask Singletons 'app' and 'db'
used by ../run.py
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


# @TODO: initialize the db_session after reading the config params
# @TODO: http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/
user = 'redidropper'
passwd = 'insecurepassword'
host = 'localhost'
db_name = 'RediDropper'

engine = db.create_engine('mysql://{}:{}@{}/{}' \
        .format(user, passwd, host, db_name))
db_session = db.scoped_session(db.sessionmaker(bind=engine))


@app.before_request
def before_request():
    """ Set a timer """
    g.start = time.time()

@app.after_request
def after_request(response):
    """
    @TODO: log how long it took to parse the request
    """
    diff = time.time() - g.start
    app.logger.debug("Exec time: {}".format(str(diff)))

#    if response.response and "__EXE_TIME__" in response.response:
#        response.response = response.response.replace(
#            '__EXE_TIME__', str(diff))
#        response.headers["content-length"] = len(response.response)

    return response

@app.teardown_request
def end_of_request(exception=None):
    """ Release resources """
    if exception is not None:
        app.logger.debug("end_of_request() exception: {}".format(exception))

    # @see http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/
    # sess = g.get('db_session', None)
    if db_session is not None:
        app.logger.debug("removing session...")
        db_session.remove()
