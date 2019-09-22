from . import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    current_start_time = db.Column(db.DateTime)
    # TODO: timezone info, user state

    records = db.relationship('Record', back_populates='user', passive_deletes=True)


class Record(db.Model):
    __tablename__ = 'records'

    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    # Always stored in UTC. However, data type is timestamp without timezone
    begin_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='records')

    def duration(self):
        return str(self.end_time - self.begin_time)

