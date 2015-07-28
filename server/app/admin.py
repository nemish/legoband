from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
import flask_wtf
from flask.ext import login
from flask import redirect, url_for, render_template

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


admin = Admin(app, name='legoband', index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(ProtectedModelView(models.Message, db.session))
admin.add_view(ProtectedModelView(models.User, db.session))
admin.add_view(ProtectedModelView(models.Page, db.session))