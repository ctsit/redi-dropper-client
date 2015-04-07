# Init the Flask Singletons 'app' and 'db'
# used by ../run.py
import sys

try:
    from flask import Flask
except ImportError, e:
    sys.exit("Missing required package: Flask")

try:
    from flask_sqlalchemy import SQLAlchemy
except ImportError, e:
    sys.exit("Missing required package: SQLAlchemy")


# The WSGI compliant web-application object
app = Flask(__name__)

# The Object-Relationan-Mapping (ORM) object
db = SQLAlchemy(app)
