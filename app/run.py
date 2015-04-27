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

ssl_public_key_file = 'server.crt'
ssl_private_key_file = 'server.key'


def get_ssl_context(app):
    """
    Get a SSL context in debug mode
    @see http://werkzeug.pocoo.org/docs/0.10/serving/#quickstart
    """
    import os.path
    import ssl

    ssl_context = None

    if app.debug:
        if os.path.isfile(ssl_public_key_file) and \
                os.path.isfile(ssl_private_key_file):
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.load_cert_chain(ssl_public_key_file,
                                        ssl_private_key_file)
        else:
            try:
                import OpenSSL
                # if the pyOpenSSL is installed use the adhoc ssl context
                ssl_context = 'adhoc'
            except:
                pass
    return ssl_context


if __name__ == "__main__":
    ssl_context = get_ssl_context(app)
    app.run(ssl_context=ssl_context)
