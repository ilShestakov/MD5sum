import urllib.parse
from .config import Config
from redis import StrictRedis, ConnectionError


def redis_set(flask):

    # Set Redis connection:
    redis_url = urllib.parse.urlparse(Config.REDIS_URL)
    r = StrictRedis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password)

    # Test the Redis connection:
    try:
        r.ping()
        print("Redis is connected")
    except ConnectionError:
        print("ERROR: Something wrong with Redis server connection.")
