#!/usr/bin/env python3
import os
from flask import Flask, request
import telebot

# TODO: config.py
TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['begin'])
def begin_interval_handler(message):
    bot.send_message(message.chat.id, text='Detected command /begin')


@bot.message_handler(commands=['end'])
def begin_interval_handler(message):
    bot.send_message(message.chat.id, text='Detected command /end')


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
