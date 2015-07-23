from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import flask_wtf

from app import app, db
from app.models import Message


class ProtectedModelView(ModelView):
    form_base_class = flask_wtf.Form

admin = Admin(app, name='legoband', template_mode='bootstrap3')
admin.add_view(ProtectedModelView(Message, db.session))