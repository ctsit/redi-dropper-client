"""
Define the routes for general pages
"""
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template

from redidropper.main import app

@app.route('/')
def index():
    """ Render the home page """
    return render_template('pages/index.html')


@app.route('/login')
def login():
    """ Render the login form """
    return render_template('pages/login.html')


@app.route('/logout')
def logout():
    """ Destroy the user session and redirect to the home page """
    session.pop('user')
    return redirect('/')


@app.route('/about')
def about():
    """ Render the about page """
    return render_template('pages/about.html')


@app.route('/contact')
def contact():
    return render_template('pages/contact.html')
