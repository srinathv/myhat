import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_PATH = os.path.join(basedir, 'database/app.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_DATABASE_PATH

SECRET_KEY = 'sosuperseriouslysecret'

