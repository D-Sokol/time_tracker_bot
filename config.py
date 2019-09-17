import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PORT = os.environ.get('PORT')
    TOKEN = os.environ['TOKEN']
