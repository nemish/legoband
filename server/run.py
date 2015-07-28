#!/Users/nemish/.virtualenvs/legoband/bin/python
# -*- coding: utf-8 -*-
import os
from app import app, db
from app.models import Page


def build_sample_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def init_default_data():
    page = Page.query.first()

if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE_PATH']):
        build_sample_db()



    app.run(debug=True)