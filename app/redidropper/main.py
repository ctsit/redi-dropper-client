"""
Goal: Init the Flask Singletons 'app' and 'db'
used by ../run.py

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
except ImportError, error:
    import sys
    sys.exit("Missing required package: {}".format(error))


# The WSGI compliant web-application object
app = Flask(__name__)

# The Object-Relationan-Mapping (ORM) object
db = SQLAlchemy(app)
