# -*- coding: utf-8 -*-
import os
from flask import url_for
from datetime import datetime
from sqlalchemy.event import listens_for
from flask_admin import form

from app import db, app
from app.util.email import send_email

class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


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


class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512))
    welcome_section_text = db.Column(db.String(512))
    slogan = db.Column(db.String(512))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(32))
    location = db.Column(db.String(512))
    footer_text = db.Column(db.String(512))
    vk_link = db.Column(db.String(128))
    facebook_link = db.Column(db.String(128))
    vimeo_link = db.Column(db.String(128))
    twitter_link = db.Column(db.String(128))

    @classmethod
    def main(cls):
        return cls.query.filter_by(url='/').first()


class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    image_path_sm = db.Column(db.String(512))
    image_path = db.Column(db.String(512))
    short_desc = db.Column(db.String(512))
    desc = db.Column(db.String(512))
    ordering = db.Column(db.Integer)

    def get_image_sm_url(self):
        return url_for('static', filename=self.image_path_sm)

    def get_image_url(self):
        return url_for('static', filename=self.image_path)


class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))
    link = db.Column(db.String(1024))


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    path = db.Column(db.String(128))

    def __unicode__(self):
        return self.name

    def get_full_image_url(self):
        return self._get_url(self.path)

    def get_thumb_url(self):
        return self._get_url(form.thumbgen_filename(self.path))

    def _get_url(self, filename):
        return url_for('static', filename=os.path.join('media', 'photo', filename))


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    title = db.Column(db.String(512))
    location = db.Column(db.String(512), nullable=True)
    description = db.Column(db.Text, nullable=True)


@listens_for(Photo, 'after_delete')
def del_image(mapper, connection, target):
    photo_path = app.config['PHOTO_FOLDER']
    if target.path:
        # Delete image
        try:
            os.remove(os.path.join(photo_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(os.path.join(photo_path, form.thumbgen_filename(target.path)))
        except OSError:
            pass

        # 'photo_gallery': [{
        #     'url': url_for('static', filename="img/photo/photo2.jpg")
        # }, {
        #     'url': url_for('static', filename="img/photo/photo3.jpg")
        # }],
