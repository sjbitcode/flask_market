import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLALCHEMY_DATABASE_URI = os.path.join(
    'sqlite:////', BASE_DIR.lstrip('/'), 'market.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
