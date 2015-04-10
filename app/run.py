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
initializer.do_init(app, db)


if __name__ == "__main__":
    # run the server if executed from the command line
    app.run()
