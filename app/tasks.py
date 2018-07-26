from .celery_ import celery
from hashlib import md5
from requests import get, exceptions
from time import sleep


@celery.task(bind=True, task_time_limit=60)
def md5_counting(self, file_url):
    #self.update_state(state=u'RUNNING', meta={'stamp': 'beginning of processing'})

    sleep(10)

    try:
        r_file = get(file_url, timeout=(10, 10))
    except MemoryError:
        return {'err': 'low_memory'}
    #except exceptions:
        #return {'err': 'requests'}

    if r_file.status_code != 200:
        return {'err': 'bad_url'}
    try:

        md5hash = md5(r_file.content).hexdigest()  # content is in bytes already
        sum = add.delay(21, 9)

    except Exception:
        return {'err': 'hashlib'}

    return {'md5': md5hash}


@celery.task(bind=True)
def add(self, x, y):
    print(' ----- ADD:', x+y)
    sleep(10)
    return x + y
