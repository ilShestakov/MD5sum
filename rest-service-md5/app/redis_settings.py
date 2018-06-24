from flask import make_response, jsonify
import urllib.parse
from redis import StrictRedis, ConnectionError


def redis_set(flask):
    @flask.errorhandler(ConnectionError) #TODO
    def redis_connect_err(error):
        return make_response(jsonify({'error': 'redis connection'}), 404)

    # Set Redis connection:
    redis_url = urllib.parse.urlparse('redis://localhost:6379/0')
    r = StrictRedis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password)

    # Test the Redis connection:
    try:
        r.ping()
        print("Redis is connected")
    except ConnectionError:
        print("ERROR: Something wrong with Redis server connection.")