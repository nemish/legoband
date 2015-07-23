# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
import flask_wtf

app = Flask(__name__)
app.config.from_object('config')

flask_wtf.CsrfProtect(app)

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)


from app import views
from app import admin

