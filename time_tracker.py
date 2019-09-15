#!/usr/bin/env python3
import os
from flask import Flask, request
import telebot

from models import db
import management

# TODO: config.py
TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(server)
# FIXME: with operator is required when using init_app, but does not when server given to db constructor.
with server.app_context():
    db.create_all()


@bot.message_handler(commands=['begin'])
def begin_interval_handler(message):
    time = management.begin_interval(message.user.id)
    bot.reply_to(message, 'New interval started at {}'.format(time.strftime('%T')))


@bot.message_handler(commands=['cancel'])
def cancel_interval_handler(message):
    management.cancel_interval(message.user.id)
    bot.reply_to(message, 'Your last begin time was cleared')


@bot.message_handler(commands=['end'])
def end_interval_handler(message):
    try:
        record = management.end_interval(message.user.id)
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
        record = management.get_last_record(message.user.id)
        bot.reply_to(message, 'Last record: {} - {} (duration {})'.format(
            record.begin_time.strftime('%T'),
            record.end_time.strftime('%T'),
            record.duration(),
        ))
    except ValueError:
        bot.reply_to(message, 'You have no any records. Use /begin and /end to add them')


@bot.message_handler(commands=['deletelast'])
def delete_last_handler(message):
    management.delete_last_record(message.user.id)
    bot.reply_to(message, 'Your last record was deleted')


@bot.message_handler(func=lambda msg: True)
def default_message_handler(message):
    # it shows structure of message object
    bot.reply_to(message, str(message.__dict__))


# TODO: move flask server creation to another module
@server.route('/')
def webhook():
    bot.remove_webhook()
    # TODO: use server.config['SERVER_NAME']
    bot.set_webhook(url='https://time-tracker-bot.herokuapp.com/{}'.format(TOKEN))
    return 'ok'


@server.route('/' + TOKEN, methods=['POST'])
def update():
    # TODO: understand this line
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode())])
    return 'ok'


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=os.environ.get('PORT'))
