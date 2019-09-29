#!/usr/bin/env python3
import tempfile

from config import Config
from server import bot, server
from database import management


@bot.message_handler(commands=['begin'])
def begin_interval_handler(message):
    time = management.begin_interval(message.from_user.id, message.date)
    bot.reply_to(message, 'New interval started at {}'.format(time))


@bot.message_handler(commands=['cancel'])
def cancel_interval_handler(message):
    management.cancel_interval(message.from_user.id)
    bot.reply_to(message, 'Your last begin time was cleared')


@bot.message_handler(commands=['end'])
def end_interval_handler(message):
    try:
        record = management.end_interval(message.from_user.id, message.date)
        # TODO: move '{} - {} (duration {})' to Record.__str__
        bot.reply_to(message, 'Record added: {} - {} (duration {})'.format(
            record.format_begin_time(),
            record.format_end_time(),
            record.duration(),
        ))
    except ValueError as e:
        bot.reply_to(message, str(e))


@bot.message_handler(commands=['userscount'])
def users_count_handler(message):
    bot.reply_to(message, 'Users: {}'.format(management.get_users_count()))


@bot.message_handler(commands=['getlast'])
def get_last_handler(message):
    try:
        record = management.get_last_record(message.from_user.id)
        bot.reply_to(message, 'Last record: {} - {} (duration {})'.format(
            record.format_begin_time(),
            record.format_end_time(),
            record.duration(),
        ))
    except ValueError:
        bot.reply_to(message, 'You have no any records. Use /begin and /end to add them')


@bot.message_handler(commands=['deletelast'])
def delete_last_handler(message):
    try:
        management.delete_last_record(message.from_user.id)
        bot.reply_to(message, 'Your last record was deleted')
    except ValueError:
        bot.reply_to(message, 'You have no any records. Use /begin and /end to add them')


@bot.message_handler(commands=['delete'])
def delete_selected_handler(message):
    msg = message.text.split()
    if len(msg) < 2 or not msg[1].isdigit():
        bot.reply_to(message, 'You have not provided record id to delete')
    else:
        record_id = int(msg[1])
        management.delete_record(record_id)
        bot.reply_to(message, f'Record #{record_id} was deleted')


@bot.message_handler(commands=['getfile'])
def get_file_handler(message):
    user = management.ensure_user(message.from_user.id)
    if not user.records:
        bot.reply_to(message, 'You have no any records. Use /begin and /end to add them')
    else:
        file = tempfile.NamedTemporaryFile(mode='w+t')
        # Since NamedTemporaryFile has special object to delete file,
        #  it is safe to set file.name to any desired value
        file.name = 'records.csv'
        management.records_to_file(user.user_id, file)
        file.seek(0)
        bot.send_document(message.chat.id, file, caption='Total records: {}'.format(len(user.records)))


# TODO: commands for timezone support


# Any testing functions I need
@bot.message_handler(func=lambda msg: True)
def default_message_handler(message):
    msg = message.text.split()
    if msg and msg[0] == Config.TOKEN:
        bot.reply_to(message, str(server.config))


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=Config.PORT)
