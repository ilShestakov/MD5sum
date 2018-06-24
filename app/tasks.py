#from app import celery
import requests
import hashlib

from .celery_ import celery


@celery.task(bind=True, task_time_limit = 60)
def md5_counting(self, url,):
    self.update_state(state = 'running')
    r_file = requests.get(url)  # file downloading
    if r_file.status_code == 404:  # TODO != 200 ?
        self.update_state(state = 'failed')
    md5hash = hashlib.md5(r_file.content).hexdigest()  # content is in bytes
    self.update_state(state = 'done')
    #  sent email TODO

    return md5hash