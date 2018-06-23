import random
import time
from flask import Flask, request, abort, make_response, render_template, session, flash, redirect, \
    url_for, jsonify
#from flask_mail import Mail, Message
#from flask_mail import Message, Mail
from celery import Celery
import requests
import hashlib


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'top-secret!'

''' mail
# Flask-Mail configuration
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'shes7akov@gmail.com',
    MAIL_PASSWORD = 'mypassword',
))
#app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'
'''

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# 'amqp://guest@localhost//'
# 'rpc://'
#redis://localhost:6379/0

#mail = Mail(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#TODO root_name
root_name = "/md5/api/v1.0"
#TODO check all response codes
#TODO returns in POST and GET f-ns

tasks = [
    {
        'id': 1,
        'url': u'http://site.com/text.txt',
        'email': u'ex@gmail.ru',
        'status': u'failed',
        'md5': None
    }
] #TODO db

ID = []

'''
@app.route('/')
@app.route('/nothing')
def nothing():
    return "just nothing"

@app.route(root_name)
def root():
    return "Hi!"
'''

def requests_test():
    r = requests.get('https://www.google.com/images/srpr/logo11w.png')

    #r.encoding
    with open('google_logo.png', 'wb') as f:
        f.write(r.content)
    print("req_test here")

def print_structure_test():
    # print(request.url_root)
    # !!!print(request.args)
    print(request.form)
    print(request.form.get('email'))
    print(request.form.get('url'))
    print(request.form.get('url', 'no url'))


@app.route(root_name + '/tasks', methods=['GET'])
def get_tasks():
    if len(tasks)== 0:
        return jsonify({'ur tasks': 'nothing'})
    return jsonify({'ur tasks': tasks})


#parametrs: url and email
@app.route(root_name + '/submit', methods=['POST'])
def create_task():
    if request.form.get('url') is None:  # no url in user request data
        abort(400)  # bad request

    file_url = request.form.get('url')

    res = md5_counting.delay(file_url)  # result!


    new_task = {
        'id': res.id,
        'url': file_url,
        'email': request.form.get(u'email', u'none'), #email or none
        #'status': None, #dont know! #u'done' if res.ready() else u'running',
        'md5': res.result
    }

    tasks.append(new_task)

    return jsonify({'id':res.id}), 201  # created



@celery.task(bind=True)
#For this task I've added a bind=True argument in the Celery decorator.
# This instructs Celery to send a self argument to my function, which I can then use to record the status updates.
def md5_counting(self, url):  #как то передать только урл
    """Background task that runs a long function with progress reports."""

    self.update_state(state = 'running')

    #выкачиваем файл по урл
    r_file = requests.get(url)  # file downloading
    if r_file.status_code == 404:  # TODO != 200 ?
        print("self failed")
        self.update_state(state = 'failed')

    md5hash = hashlib.md5(r_file.content).hexdigest()  # content is in bytes

    #  # sent email TODO

    self.update_state(state = 'done')

    return md5hash


# GET
@app.route(root_name + "/check", methods=['GET'])
def get_task():
    if request.args.get('id') is None:  # no id in user url request
        abort(400)  # bad request

    requested_id = request.args.get('id', -1) #TODO hmmm

    print('requested id ', request.args.get('id', -1))

    task = md5_counting.AsyncResult(requested_id)
    return jsonify({"status": task.status, "md5": task.result})

'''depricated
    for task in tasks:
        if task['id'] == requested_id: #TODO TYPES ??
            print("found")
            return jsonify({'status': task['status']})
  #  print(request.args)
    return jsonify({"status":"doesnt exist"})
'''

if __name__ == '__main__':
    app.run(debug=True)
