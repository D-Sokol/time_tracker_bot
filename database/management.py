from datetime import datetime

from . import session
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
    return record


def delete_record(record_id):
    record = Record.query.get(record_id)
    if record:
        session.delete(record)
        session.commit()


def get_last_record(user_id):
    records = ensure_user(user_id).records
    if records:
        return records[-1]
    raise ValueError('Not found')


# Functions, realizing bot's commands
def begin_interval(user_id, time=None):
    user = ensure_user(user_id)
    user.current_start_time = time or datetime.now()
    session.commit()
    return user.current_start_time


def cancel_interval(user_id):
    user = ensure_user(user_id)
    user.current_start_time = None
    session.commit()


def end_interval(user_id, end_time=None):
    user = ensure_user(user_id)
    start_time = user.current_start_time
    if start_time is None:
        # TODO: custom exceptions
        raise ValueError('Cannot end interval without start')
    user.current_start_time = None
    return create_record(user_id, start_time, end_time or datetime.now())


def delete_last_record(user_id):
    session.delete(get_last_record(user_id))
    session.commit()


def get_users_count():
    return User.query.count()


def records_to_file(user_id):
    records = ensure_user(user_id).records
    if not records:
        return None

    return '\n'.join(
        f'{record.record_id},"{record.begin_time}","{record.end_time}",{record.duration()}'
        for record in records
    )
