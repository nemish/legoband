#!/Users/nemish/.virtualenvs/legoband/bin/python
# -*- coding: utf-8 -*-
import os
from app import app, db


def build_sample_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE_PATH']):
        build_sample_db()

    app.run(debug=True)