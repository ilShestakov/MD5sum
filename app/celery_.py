from celery import Celery
from .config import Config
from app import flask

celery = Celery('app',
                broker=Config.CELERY_BROKER_URL,
                backend=Config.CELERY_RESULT_BACKEND,
                include=['app.tasks'])

celery.conf.update(flask.config)

if __name__ == '__main__':
    celery.start()