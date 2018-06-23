from flask import Flask, request, abort, make_response, jsonify
from celery import Celery
#from flask_mail import Mail, Message
import requests
import hashlib
import redis_settings
import flask_routes
import time

#TODO check all response codes
#TODO mail integration


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'top-secret!'


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# 'amqp://guest@localhost//'
# 'rpc://'   #redis://localhost:6379/0


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


tasks = [
    {
        'id': 0,
        'url': u'http://site.com/text.txt',
        'email': u'ex@gmail.ru',
    }
]


redis_settings.redis_set(app)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    if len(tasks) == 0:
        return jsonify({'ur tasks': 'nothing'})

    return jsonify({'ur tasks': tasks})


@app.route('/submit', methods=['POST'])
def create_task():
    file_url = request.form.get('url')
    if file_url is None:  # no url in user request data
        abort(400)  # bad request
    res = md5_counting.delay(file_url)
    #time.sleep(5)
    new_task = {
         'id': res.id,
         'url': file_url,
         'email': request.form.get(u'email', u'none'), #email or none
     }
    tasks.append(new_task)

    return jsonify({'id':res.id}), 201  # created


@celery.task(bind=True)
def md5_counting(self, url,):
    self.update_state(state = 'running')
    r_file = requests.get(url)  # file downloading
    if r_file.status_code == 404:  # TODO != 200 ?
        self.update_state(state = 'failed')
    md5hash = hashlib.md5(r_file.content).hexdigest()  # content is in bytes
    self.update_state(state = 'done')
    #  sent email TODO

    return md5hash


@app.route('/check', methods=['GET'])
def get_task():
    if request.args.get('id') is None:  # no id in user request
        abort(400)  # bad request
    requested_id = request.args.get('id', -1) #TODO hmmm
    task = md5_counting.AsyncResult(requested_id)
    return jsonify({"status": task.status, "md5": task.result})


if __name__ == '__main__':
    app.run(debug=True)
