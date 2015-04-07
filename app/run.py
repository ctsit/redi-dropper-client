from redidropper.main import app, db
from redidropper.startup import initializer

# Configures routes, models
initializer.do_init(app, db)


# run the server if executed from the command line
if __name__ == "__main__":
    # @TODO: load config.py
    app.run(port=5000, debug=True)
