class Config(object):
    # Flask setup
    SECRET_KEY = 'super_secret_key'

    # Celery setup:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_IGNORE_RESULT = False

    # Redis setup:
    REDIS_HOST = 'localhost'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    REDIS_URL = 'redis://localhost:6379/0'
    REDIS_SOCKET_TIMEOUT = 10000

    # Mail setup
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'md5counting@gmail.com'
    MAIL_PASSWORD = 'md5toyourhome'
    MAIL_DEFAULT_SENDER = 'md5counting@gmail.com'
