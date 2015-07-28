# -*- coding: utf-8 -*-
from flask import render_template, url_for, request, jsonify

from app import app, db
from app.forms import ContactForm, LoginForm
from app.models import Message


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


@app.route('/contact_me/', methods=['POST'])
def contact_me():
    form = ContactForm(request.form)
    if form.validate_on_submit():
        message = Message(
            name=form.data['name'],
            phone=form.data['phone'],
            email=form.data['email'],
            message=form.data['message']
        )
        db.session.add(message)
        db.session.commit()
        message.notify()
        return jsonify(message=u'Спасибо, мы с вами свяжемся.')
    return jsonify(form.errors)


# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         pass
#         # user = User.
#     return render_template('login.html', form=form)
