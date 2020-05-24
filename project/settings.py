import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLALCHEMY_DATABASE_URI = 'sqlite:///market.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
