import os

class Config(object):
    redis_port = 6380

    # Flask setup
    SECRET_KEY = 'super_secret_key'

    # Celery setup:
    CELERY_BROKER_URL = 'amqp://ivanmq:qwemq@localhost:5672/myvhost'.format(
        #os.environ.get('RABBITMQ_DEFAULT_USER', 'admin'),
        #os.environ.get('RABBITMQ_DEFAULT_PASS', 'mypass')
        )

    #CELERY_BROKER_URL = 'redis://localhost:' + str(redis_port) + '/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:' + str(redis_port)+ '/0'
    CELERY_IGNORE_RESULT = False

    # Redis setup:
    REDIS_HOST = 'localhost'
    REDIS_PASSWORD = ''
    REDIS_PORT = redis_port
    REDIS_URL = 'redis://localhost:' + str(redis_port) + '/0'
    REDIS_SOCKET_TIMEOUT = 10000

