# -*- coding: utf-8 -*-
from flask import render_template, url_for, request, jsonify, redirect
from sqlalchemy import or_

from app import app, db
from app.forms import ContactForm
from app.models import Message, Page, Staff, Video, Photo


@app.route('/')
def index():
    if app.config['OFF']:
        return redirect(url_for('maintanance'))

    index_page_data = {
        'staff': Staff.query.order_by(Staff.ordering),
        'photos': Photo.query.filter(or_(Photo.path != None, Photo.path != '')),
        'contact_form': ContactForm(),
        'page': Page.main(),
        'videos': Video.query.all()
    }
    return render_template('index.html', **index_page_data)


@app.route('/maintanance')
def maintanance():
    return render_template('maintanance.html')


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
        return jsonify({
            'status': 'success',
            'message': u'Спасибо, мы с вами свяжемся.'
        })
    response = {
        'status': 'failure',
    }
    response.update(form.errors)
    return jsonify(response)
