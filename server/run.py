#!/Users/nemish/.virtualenvs/legoband/bin/python
# -*- coding: utf-8 -*-
import os
from app import app, db
from app.models import Page, User, Staff, Video


def init():
    try:
        os.mkdir(app.config['PHOTO_FOLDER'])
    except OSError:
        pass


def build_sample_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    init_default_data()


def init_default_data():
    main_page_exists_query = db.session.query(Page).filter(Page.url == '/').exists()
    main_page_exists = db.session.query(main_page_exists_query).scalar()
    if not main_page_exists:
        page = Page(
            url='/',
            welcome_section_text=u'Акустический кавер-проект, от которого вам станет хорошо',
            slogan=u'Надеемся, вы любите хорошую музыку так же как и мы :)',
            phone='8-926-123-54-67',
            email='welcome@legoband.ru',
            location=u'Москва',
            footer_text=u'Корпоративы, праздники, дни рождения и прочее прочее веселье.',
            vimeo_link='#',
            facebook_link='#',
            vk_link='#'
        )
        user = User(name=u'Ярослав', email='nemish.i.nelos@gmail.com', password='Djh231GHDfk')
        db.session.add(page)
        db.session.add(user)

    staff_exists_query = db.session.query(Staff).exists()
    staff_exists = db.session.query(staff_exists_query).scalar()
    if not staff_exists:
        staff_data_list = [{
            'id': 1,
            'image_path_sm': "img/staff_1_sm.jpg",
            'name': u'Имя Фамилия',
            'short_desc': u'Первый случай в истории, когда человек родился с кахоном в руках',
            'desc': u'Тестовый текст про участника и всякое такое',
            'image_path': "img/staff_1.jpg"
        }, {
            'id': 2,
            'image_path_sm': "img/staff_2_sm.jpg",
            'name': u'Имя Фамилия',
            'short_desc': u'С помощью бас-гитары играет на струнках вашей души',
            'image_path': "img/staff_2.jpg",
            'desc': u'Тестовый текст про участника и всякое такое'
        }, {
            'id': 3,
            'image_path_sm': "img/staff_3_sm.jpg",
            'name': u'Наташа Павлова',
            'short_desc': u'На гитаре может слабать все от Хендрикса до Цоя',
            'image_path': "img/staff_3.jpg",
            'desc': u'Тестовый текст про участника и всякое такое'
        }, {
            'id': 4,
            'image_path_sm': "img/staff_4_sm.jpg",
            'name': u'Имя Фамилия',
            'short_desc': u'От ее голоса стаканы не лопаются, а склеиваются обратно',
            'image_path': "img/staff_4.jpg",
            'desc': u'Тестовый текст про участника и всякое такое'
        }]
        for artist_data in staff_data_list:
            db.session.add(Staff(**artist_data))

    video_exists_query = db.session.query(Video).exists()
    video_exists = db.session.query(video_exists_query).scalar()
    if not video_exists:
        video = Video(
            text=u'Посмотрите наше промо видео',
            link='https://vimeo.com/125882554'
        )
        db.session.add(video)

    db.session.commit()

if __name__ == '__main__':
    init()
    if not os.path.exists(app.config['DATABASE_PATH']):
        build_sample_db()
    init_default_data()

    app.run(debug=True)