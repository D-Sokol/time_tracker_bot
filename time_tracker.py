#!/usr/bin/env python3
from config import Config
from server import bot, server
from database import management


@bot.message_handler(commands=['begin'])
def begin_interval_handler(message):
    time = management.begin_interval(message.from_user.id)
    bot.reply_to(message, 'New interval started at {}'.format(time.strftime('%T')))


@bot.message_handler(commands=['cancel'])
def cancel_interval_handler(message):
    management.cancel_interval(message.from_user.id)
    bot.reply_to(message, 'Your last begin time was cleared')


@bot.message_handler(commands=['end'])
def end_interval_handler(message):
    try:
        record = management.end_interval(message.from_user.id)
        # TODO: move '{} - {} (duration {})' to Record.__str__
        bot.reply_to(message, 'Record added: {} - {} (duration {})'.format(
            record.begin_time.strftime('%T'),
            record.end_time.strftime('%T'),
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
            record.begin_time.strftime('%T'),
            record.end_time.strftime('%T'),
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
    data = management.records_to_file(message.from_user.id)
    if data is None:
        bot.reply_to(message, 'You have no any records. Use /begin and /end to add them')
    else:
        bot.send_document(message.chat.id, data.encode(), caption='Records.csv')


# Any testing functions I need
@bot.message_handler(func=lambda msg: True)
def default_message_handler(message):
    msg = message.text.split()
    if msg and msg[0] == Config.TOKEN:
        bot.reply_to(message, str(server.config))


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=Config.PORT)
