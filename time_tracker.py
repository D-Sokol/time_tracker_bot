#!/usr/bin/env python3
import os
from flask import Flask, request
import telebot

from models import db

# TODO: config.py
TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

@bot.message_handler(func=lambda msg: True)
def default_message_handler(message):
    # it shows structure of message object
    bot.reply_to(message, str(message.__dict__))


# TODO: move flask server creation to another module
@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://time-tracker-bot.herokuapp.com/{}'.format(TOKEN))
    return 'ok'


@server.route('/' + TOKEN, methods=['POST'])
def update():
    # TODO: understand this line
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode())])
    return 'ok'


if __name__ == '__main__':
    db.init_app(server)
    # FIXME: with operator is required when using init_app, but does not when server given to db constructor.
    with server.app_context():
        db.create_all()
    server.run()
