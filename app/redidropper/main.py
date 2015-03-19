# Init the Flask Singletons 'app' and 'db'
# used by ../run.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# The WSGI compliant web-application object
app = Flask(__name__)

# The Object-Relationan-Mapping (ORM) object
db = SQLAlchemy(app)
