# -*- coding: utf-8 -*-
from datetime import date
from flask import render_template, url_for, request, jsonify, redirect
from sqlalchemy import or_

from app import app, db
from app.forms import ContactForm
from app.models import Message, Page, Staff, Video, Photo, Event


@app.route('/')
def index():
    if app.config['OFF']:
        return redirect(url_for('maintanance'))

    events = Event.query.filter(Event.date >= date.today()).order_by(Event.date)[:6]
    events_count = len(events)
    index_page_data = {
        'staff': Staff.query.order_by(Staff.ordering),
        'photos': Photo.query.filter(or_(Photo.path != None, Photo.path != '')),
        'contact_form': ContactForm(),
        'page': Page.main(),
        'videos': Video.query.all(),
        'events': [[events[i], events[i+1] if i < events_count - 1 else None] for i in xrange(0, events_count, 2)]
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
        return jsonify({
            'status': 'success',
            'message': u'Спасибо, мы с вами свяжемся.'
        })
    response = {
        'status': 'failure',
    }
    response.update(form.errors)
    return jsonify(response)
