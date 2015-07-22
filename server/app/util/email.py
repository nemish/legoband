# -*- coding: utf-8 -*-
from datetime import datetime
from app.util.decorators import async
from app import app, mail, db
from flask.ext.mail import Message
from config import ADMINS


@async
def _send_async(app, email, callback=None):
    with app.app_context():
        mail.send(email)
        if callback:
            callback()


def send_email(subject, text_body, html_body, callback=None):
    email = Message(subject, sender=ADMINS[0], recipients=ADMINS)
    email.body = text_body
    email.html = html_body
    _send_async(app, email, callback)
