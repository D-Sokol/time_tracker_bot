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


# Any testing functions I need
@bot.message_handler(func=lambda msg: True)
def default_message_handler(message):
    if msg.split()[0] == Config.TOKEN:
        bot.reply_to(message, str(app.config))


if __name__ == '__main__':
    server.run(host='0.0.0.0')
