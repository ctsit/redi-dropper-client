"""
Goal: Implement the application entry point

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

from redidropper.main import app, mail
from redidropper.startup import initializer

# Configures routes, models
app = initializer.do_init(app)
mail.init_app(app)


if __name__ == "__main__":
    """ Entry point for command line execution """
    ssl_context = initializer.get_ssl_context(app)
    app.run(ssl_context=ssl_context)
