#!/usr/bin/env python3
import os
import telebot

bot = telebot.TeleBot(os.environ.get('TOKEN'))

# FIXME: it is possible to have 0 filters?
@bot.message_handler()
def default_message_handler(message):
    # it shows structure of message object
    bot.reply_to(message, str(message.__dict__))


bot.polling()
