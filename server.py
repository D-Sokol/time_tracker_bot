from flask import Flask, request
from flask_migrate import Migrate
import telebot

from config import Config
from database import db


migrate = Migrate()

def create_server(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    return app

server = create_server()
bot = telebot.TeleBot(server.config['TOKEN'])


@server.route('/')
def webhook():
    bot.remove_webhook()
    # TODO: use server.config['SERVER_NAME']
    bot.set_webhook(url='https://{}/{}'.format(Config.HOST, TOKEN))
    return 'ok'


@server.route('/' + server.config['TOKEN'], methods=['POST'])
def update():
    # TODO: understand this line
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode())])
    return 'ok'

