import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN = os.environ.get('TOKEN', 'random_string')
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
