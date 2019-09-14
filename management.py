from .models import session
from .models import User, Record


def ensure_user(chat_id):
    user = User.query.get(chat_id)
    if user:
        return user
    user = User(user_id=chat_id)
    session.add(user)
    session.commit()
    return user


def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        session.delete(user)
        session.commit()


def create_record(user_id, begin_time, end_time):
    record = Record(user_id=user_id, begin_time=begin_time, end_time=end_time)
    session.add(record)
    session.commit()


def delete_record(record_id):
    record = Record.query.get(record_id)
    if record:
        session.delete(record)
        session.commit()
