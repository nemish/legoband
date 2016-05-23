from app import app, db
from app.models import Message


def send():
    msgs = Message.query.filter(Message.send_on=None)
    for msg in msgs:
        print 'sending msg', msg.id
        msg.notify()


if __name__ == '__main__':
    print 'sending'
    send()
