from flask_sqlalchemy import SQLAlchemy

# TODO: remove circular import
import time_tracker

# TODO: config.py
time_tracker.server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(time_tracker.server)
session = db.session

