from flask import request, abort, make_response, jsonify
from celery import Celery
#from flask_mail import Mail, Message
import requests
import hashlib

from app import flask, redis_settings, tasks
#from app import celery

@flask.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


redis_settings.redis_set(flask)


tasks2 = [
    {
        'id': 0,
        'url': u'http://site.com/text.txt',
        'email': u'ex@gmail.ru',
    }
]

@flask.route('/tasks', methods=['GET'])
def get_tasks():
    if len(tasks2) == 0:
        return jsonify({'ur tasks': 'nothing'})

    return jsonify({'ur tasks': tasks2})


@flask.route('/submit', methods=['POST'])
def create_task():
    file_url = request.form.get('url')
    if file_url is None:  # no url in user request data
        abort(400)  # bad request
    res = tasks.md5_counting.delay(file_url)
    #time.sleep(5)
    new_task = {
         'id': res.id,
         'url': file_url,
         'email': request.form.get(u'email', u'none'), #email or none
     }
    tasks2.append(new_task)

    return jsonify({'id':res.id}), 201  # created




@flask.route('/check', methods=['GET'])
def get_task():
    if request.args.get('id') is None:  # no id in user request
        abort(400)  # bad request
    requested_id = request.args.get('id', -1) #TODO hmmm
    task = tasks.md5_counting.AsyncResult(requested_id)
    return jsonify({"status": task.status, "md5": task.result, })