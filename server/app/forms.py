# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, StringField, TextAreaField, PasswordField
from wtforms.validators import Required, Email, ValidationError

from app.models import User


class ContactForm(Form):
    name = StringField(label=u'Имя', validators=[Required()])
    email = TextField(label=u'Email')
    phone = StringField(label=u'Телефон', validators=[Required()])
    message = TextAreaField(label=u'Сообщение')
    recaptcha = RecaptchaField()


class LoginForm(Form):
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])

    def validate_email(self, field):
        user = self.get_user()
        if user is None:
            raise ValidationError(u'Пользователь с таким email\'ом не существует')

        if user.password != self.data['password']:
            raise ValidationError(u'Неверный пароль')

    def get_user(self):
        return User.query.filter_by(email=self.data['email']).first()