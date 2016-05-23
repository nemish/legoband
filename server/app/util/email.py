# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD


def send_email(subject, body, callback=None):
    import smtplib

    # Prepare actual message
    message = u'\From: {}\nTo: {}\nSubject: {}\n\n{}'.format(MAIL_USERNAME, ", ".join(ADMINS), subject, body).encode('utf8')

    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(MAIL_USERNAME, MAIL_PASSWORD)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(MAIL_USERNAME, ADMINS, message)
        #server_ssl.quit()
        server_ssl.close()

        if callback:
            callback()

        print 'successfully sent the mail'
    except:
        print "failed to send mail"
