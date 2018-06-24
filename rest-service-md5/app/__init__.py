from flask import Flask
from celery import Celery

flask = Flask(__name__)

flask.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
flask.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

#celery = Celery(flask.name, broker=flask.config['CELERY_BROKER_URL'])
#celery.conf.update(flask.config)

from app import routes