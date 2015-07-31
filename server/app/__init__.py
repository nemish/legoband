# -*- coding: utf-8 -*-

from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
import flask_wtf

app = Flask(__name__)
app.config.from_object('config')

app.jinja_env.line_statement_prefix = '#'

flask_wtf.CsrfProtect(app)

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.context_processor
def utility_processor():
    def get_url(filename):
        return url_for('static', filename=filename)
    return dict(get_url=get_url)


from app import views
from app import admin


