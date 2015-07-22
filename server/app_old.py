#!/Users/nemish/.virtualenvs/legoband/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators

from flask.ext.wtf import Form
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash


# Create Flask application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '6e0bad90aeb5f910b7b68b146ecd4395'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)




# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.query.filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    email = fields.TextField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if User.query.filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


class DataValidatedInput(fields.StringField):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(DataValidatedInput, self).__call__(field, **kwargs)


class ContactForm(Form):
    name = fields.StringField(label=u'Имя', validators=[validators.DataRequired()])
    email = fields.TextField()
    phone = fields.StringField(validators=[validators.DataRequired()])
    message = fields.TextAreaField()


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated()


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


# Flask views
@app.route('/')
def index():
    index_page_data = {
        'staff': [{
            'id': 3,
            'small_img_url': url_for('static', filename="img/staff_3_sm.jpg"),
            'name': u'Наташа Павлова',
            'desc': u'На гитаре может слабать все от Хендрикса до Цоя'
        }, {
            'id': 2,
            'small_img_url': url_for('static', filename="img/staff_2_sm.jpg"),
            'name': u'Имя Фамилия',
            'desc': u'С помощью бас-гитары играет на струнках вашей души'
        }, {
            'id': 4,
            'small_img_url': url_for('static', filename="img/staff_4_sm.jpg"),
            'name': u'Имя Фамилия',
            'desc': u'От ее голоса стаканы не лопаются, а склеиваются обратно'
        }, {
            'id': 1,
            'small_img_url': url_for('static', filename="img/staff_1_sm.jpg"),
            'name': u'Имя Фамилия',
            'desc': u'Первый случай в истории, когда человек родился с кахоном в руках'
        }],
        'photo_gallery': [{
            'url': url_for('static', filename="img/photo/photo2.jpg")
        }, {
            'url': url_for('static', filename="img/photo/photo3.jpg")
        }],
        'staff_modals': [{
            'id': 1,
            'photo_url': url_for('static', filename="img/staff_1.jpg"),
            'name': u'Имя Фамилия',
            'text': u'Тестовый текст про участника и всякое такое'
        }, {
            'id': 2,
            'photo_url': url_for('static', filename="img/staff_2.jpg"),
            'name': u'Имя Фамилия',
            'text': u'Тестовый текст про участника и всякое такое'
        }, {
            'id': 3,
            'photo_url': url_for('static', filename="img/staff_3.jpg"),
            'name': u'Наташа Павлова',
            'text': u'Тестовый текст про участника и всякое такое'
        }, {
            'id': 4,
            'photo_url': url_for('static', filename="img/staff_4.jpg"),
            'name': u'Имя Фамилия',
            'text': u'Тестовый текст про участника и всякое такое'
        }],
        'contact_form': ContactForm()
    }
    return render_template('index.html', **index_page_data)

# Initialize flask-login
init_login()

# Create admin
admin = admin.Admin(app, 'Example: Auth', index_view=MyAdminIndexView(), base_template='my_master.html')

# Add view
admin.add_view(MyModelView(User, db.session))


def build_sample_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)