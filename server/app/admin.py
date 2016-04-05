from flask_admin import Admin, AdminIndexView, expose, form
from flask_admin.contrib.sqla import ModelView
import flask_wtf
from flask.ext import login
from flask import redirect, url_for, render_template
from jinja2 import Markup

from app import app, db
from app import models
from app.forms import LoginForm


class ProtectedModelView(ModelView):
    form_base_class = flask_wtf.Form

    def is_accessible(self):
        return login.current_user.is_authenticated()


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = form.get_user()
            login.login_user(user)
            if login.current_user.is_authenticated():
                return redirect(url_for('.index'))
        return render_template('login.html', form=form, errors=form.errors)

    @expose('/logout/')
    def logout(self):
        login.logout_user()
        return redirect(url_for('.index'))


class ImageView(ProtectedModelView):

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % model.get_thumb_url())

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image', base_path=app.config['PHOTO_FOLDER'], thumbnail_size=(100, 100, True))
    }


admin = Admin(app, name='legoband', index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(ProtectedModelView(models.Message, db.session))
admin.add_view(ProtectedModelView(models.User, db.session))
admin.add_view(ProtectedModelView(models.Staff, db.session))
admin.add_view(ProtectedModelView(models.Page, db.session))
admin.add_view(ProtectedModelView(models.Video, db.session))
admin.add_view(ProtectedModelView(models.Event, db.session))
admin.add_view(ImageView(models.Photo, db.session))