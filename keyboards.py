from telebot import types


keyboard_notstarted = types.ReplyKeyboardMarkup(row_width=2)
keyboard_notstarted.row('Begin interval')
keyboard_notstarted.row('Last record', 'File', 'My timezone')


keyboard_started = types.ReplyKeyboardMarkup(row_width=2)
keyboard_started.row('End interval', 'Cancel interval')
keyboard_started.row('Last record', 'File', 'My timezone')


def text_trigger(text):
    """
    Factory of function which can be used in bot.message_handler decorators instead of long lambda expression.
    """
    def handle(message):
        return message.content_type == 'text' and message.text == text
    return handle
