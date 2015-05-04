"""
Goal: implement helper class for sending emails

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>

@see: http://flask.pocoo.org/snippets/85/
"""

from flask import render_template
from flask_mail import Message
from redidropper.main import app, mail


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Helper for sending specific emails
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    try:
        mail.send(msg)
    except Exception as exc:
        print mail.__repr__
        app.logger.debug("Error sending email [{}] to [{}] due: {}"
                         .format(subject, recipients, exc))
        raise


def send_verification_email(user):
    """
    Email the token with which the user can confirm the email on the account
    """
    subject = "RediDropper Email Verification"
    sender = app.config['MAIL_SENDER_SUPPORT']
    recipient = user.email
    text_body = render_template(
        "verification_email.txt",
        sender=sender,
        user=user)
    html_body = render_template(
        "verification_email.html",
        sender=sender,
        user=user)
    send_email(subject, sender, [recipient], text_body, html_body)
