import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN = os.environ['TOKEN']
    PORT = os.environ.get('PORT')
