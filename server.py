from flask import Flask, request
from flask_migrate import Migrate
import telebot

from config import Config
from database import db


TOKEN = Config.TOKEN

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
server.config.from_object(Config)

db.init_app(server)
# db.app does not set in init_app, but set in __init__
db.app = server
db.create_all()

migrate = Migrate(server, db)

@server.route('/')
def webhook():
    bot.remove_webhook()
    # TODO: use server.config['SERVER_NAME']
    bot.set_webhook(url='https://{}/{}'.format(Config.HOST, TOKEN))
    return 'ok'


@server.route('/' + TOKEN, methods=['POST'])
def update():
    # TODO: understand this line
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode())])
    return 'ok'

