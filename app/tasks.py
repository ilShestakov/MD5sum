from .celery_ import celery
from hashlib import md5
from requests import get, exceptions
from app import mail


@celery.task(bind=True, task_time_limit=60)
def md5_counting(self, file_url, email):
    self.update_state(state=u'RUNNING', meta={'stamp': 'beginning of processing'})

    try:
        r_file = get(file_url, timeout=(10, 10))
    except MemoryError:
        return {'err': 'low_memory'}
    #except exceptions:
        #return {'err': 'requests'}
    else:
        requests_code = r_file.status_code
        if requests_code != 200:
            return {'err': 'bad_url'}

        try:
            md5hash = md5(r_file.content).hexdigest()  # content is in bytes already
        except Exception:
            return {'err': 'hashlib'}
        else:

            if email not in [None, '']:
                print("INSIDE MAIL")
                mail.sending_mail(email, file_url, md5hash)

        return {'md5': md5hash, 'url': file_url}



