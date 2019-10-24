from telebot import types


keyboard_notstarted = types.ReplyKeyboardMarkup()
keyboard_notstarted.row('Begin interval')
keyboard_notstarted.row('Last record', 'File', 'My timezone')


keyboard_started = types.ReplyKeyboardMarkup()
keyboard_started.row('End interval', 'Cancel interval')
keyboard_notstarted.row('Last record', 'File', 'My timezone')

