"""
Goal: Provide access to a database session.

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>


@see invokation of session_scope() in run.py
@see
    http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/
    db_session = db.scoped_session(Session)
"""

from contextlib import contextmanager
from redidropper.main import app, db

# the DB_ENGINE_URI is set in run#initializer.do_init()
engine = db.create_engine(app.config['DB_ENGINE_URI'], pool_size=20)

# create a factory
Session = db.sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
