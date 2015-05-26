"""
Goal: Implement the application entry point

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
"""

import os.path
import ssl

from redidropper.main import app, db, mail
from redidropper.startup import initializer

# Configures routes, models
app = initializer.do_init(app, db)
mail.init_app(app)


def get_ssl_context(app):
    """
    Get a SSL context in debug mode
    @see http://werkzeug.pocoo.org/docs/0.10/serving/#quickstart
    """
    ssl_public_key_file = app.config['SERVER_SSL_CRT_FILE']
    ssl_private_key_file = app.config['SERVER_SSL_KEY_FILE']
    ssl_context = None

    if os.path.isfile(ssl_public_key_file) and \
            os.path.isfile(ssl_private_key_file):
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.load_cert_chain(ssl_public_key_file,
                                        ssl_private_key_file)
            app.logger.warn('Using ssl certificate {}'
                    .format(ssl_public_key_file))
        except Exception as exc:
            app.logger.error("Problem loading SSL certificate: {}".format(exc))
    elif app.debug:
        try:
	    import OpenSSL
	    # if the pyOpenSSL is installed use the adhoc ssl context
	    ssl_context = 'adhoc'
	except:
	    pass

    return ssl_context


if __name__ == "__main__":
    ssl_context = get_ssl_context(app)
    # app.run(host='0.0.0.0', port=5000, ssl_context=ssl_context)
    # app.run(host='0.0.0.0', port=8080, ssl_context=ssl_context)
    app.run(ssl_context=ssl_context)
