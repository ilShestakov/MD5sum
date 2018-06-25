from flask import Flask
from .config import Config

flask = Flask(__name__)
flask.config.from_object(Config)

from app import routes


#  TODO
#  raising requests exceptions!
#  mailing is a next task in chain
#  MemoryError Solution
#
