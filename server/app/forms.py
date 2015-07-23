# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, StringField, TextAreaField, PasswordField
from wtforms.validators import Required, Email


class ContactForm(Form):
    name = StringField(label=u'Имя', validators=[Required()])
    email = TextField(label=u'Email', validators=[Email()])
    phone = StringField(label=u'Телефон', validators=[Required()])
    message = TextAreaField(label=u'Сообщение')
    recaptcha = RecaptchaField()


class LoginForm(Form):
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])

# class RegisterForm(Form):
#   name = TextField('NickName', [Required()])
#   email = TextField('Email address', [Required(), Email()])
#   password = PasswordField('Password', [Required()])
#   confirm = PasswordField('Repeat Password', [
#       Required(),
#       EqualTo('password', message='Passwords must match')
#       ])
#   accept_tos = BooleanField('I accept the TOS', [Required()])
#   recaptcha = RecaptchaField()