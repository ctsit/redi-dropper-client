"""
Goal: Implement the application entry point

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

from redidropper.main import app, db
from redidropper.startup import initializer


# Configures routes, models
app = initializer.do_init(app, db)


if __name__ == "__main__":
    from redidropper.startup import database_manager

    # run the server if executed from the command line
    with database_manager.session_scope() as session:
        app.db_session = session
        app.run()
