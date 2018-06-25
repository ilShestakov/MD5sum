
# Работает, если вписать правильные адреса и пароль
#

import os
import time
from flask import Flask
from flask_mail import Mail, Message


app = Flask(__name__)


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'md5counting@gmail.com',
    MAIL_PASSWORD = 'md5toyourhome',
))


mail = Mail(app)

# Flask-Mail configuration
#app.config['MAIL_SERVER'] = 'smtp.gmail.com'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = 'asd'  # os.environ.get('MAIL_USERNAME')
#app.config['MAIL_PASSWORD'] = 'qwe'  # os.environ.get('MAIL_PASSWORD')
#app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'



def index():

    email = 'shes7akov@gmail.com'
    print('email:', email)
    #session['email'] = email

    # send the email
    msg = Message("Доброго дня", sender = 'md5counting@gmail.com', recipients=[email])

    msg.body = "Вас Питон беспокоит"

    print(msg.recipients)

    with app.app_context():
        mail.send(msg)

    #send_async_email(msg)
    #flash('Sending email to {0}'.format(email))

    return 0



def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'
    index()