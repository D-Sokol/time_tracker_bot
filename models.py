from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
session = db.session


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    current_start_time = db.Column(db.Time)
    #TODO: timezone info, user state

    records = db.relationship('Record', back_populates='user')


class Record(db.Model):
    __tablename__ = 'records'

    record_id = db.Column(db.Integer, primary_key=True)
    used_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    begin_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    user = db.relationship('User', back_populates='records')

    def duration(self):
        raise NotImplementedError

