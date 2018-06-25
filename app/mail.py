from app import flask
from flask_mail import Mail, Message


mail = Mail(flask)


def sending_mail(email, file_url, md5):
    msg = Message('Your MD5',
                  sender='md5counting@gmail.com',
                  recipients=[email])

    msg.body = 'MD5 is %(md5)s for file from %(url)s' \
               % {'url': file_url, 'md5': md5}
    try:
        with flask.app_context():
            mail.send(msg)
    except Exception:
        print('!Something wrong with sending message')

