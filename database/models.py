from . import db
from .timezone import get_timezone, convert_to_tz


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    current_start_time = db.Column(db.DateTime)
    timezone = db.Column(db.String(30), nullable=False, server_default='UTC')

    def wrap_time(self, dt):
        tz = get_timezone(self.timezone)
        return convert_to_tz(dt, tz).strftime('%T')


class Record(db.Model):
    __tablename__ = 'records'

    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    # Always stored in UTC. However, data type is timestamp without timezone
    begin_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('records', cascade='delete'))

    def format_begin_time(self):
        return self.user.wrap_time(self.begin_time)

    def format_end_time(self):
        return self.user.wrap_time(self.end_time)

    def duration(self):
        return str(self.end_time - self.begin_time)

