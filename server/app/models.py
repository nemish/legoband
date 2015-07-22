# -*- coding: utf-8 -*-
from datetime import datetime

from app import db
from app.util.email import send_email

class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))


class Message(db.Model):

    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(1024))
    sent_on = db.Column(db.DateTime)

    def notify(self):
        send_email(
            u'Legoband.ru - новая заявка',
            self.get_body(),
            self.get_html_body(),
            self.set_notified
        )

    def set_notified(self):
        self.sent_on = datetime.now()
        db.session.add(self)
        db.session.commit()

    def get_body(self):
        return self._get_joined_string('\n')

    def get_html_body(self):
        return self._get_joined_string('<br>')

    def _get_joined_string(self, join_str):
        return join_str.join([
            u'Имя: {}'.format(self.name),
            u'Email: {}'.format(self.email),
            u'Телефон: {}'.format(self.phone),
            u'Сообщение: {}'.format(self.message)
        ])
