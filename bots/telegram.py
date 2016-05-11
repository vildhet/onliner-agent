import telebot
import logging
import pickle


_bot = None
_subscribers = []


TELEGRAM_DB = "telegram.data"


def init(config):
    global _bot
    global _subscribers

    try:
        _subscribers = pickle.load(open(TELEGRAM_DB, 'rb'))
    except (IOError, EOFError):
        pass

    logging.info('init telegram bot')
    _bot = telebot.AsyncTeleBot(config['token'])

    @_bot.message_handler(commands=['help'])
    def send_welcome(message):
        _bot.reply_to(message, "Hello I am a smart real estate agent")

    @_bot.message_handler(commands=['start'])
    def send_welcome(message):
        logging.info('client %d subscribed' % message.chat.id)
        if message.chat.id not in _subscribers:
            _subscribers.append(message.chat.id)
        _bot.reply_to(message, "You have subscribed to apartments news channel")


def get_name():
    return "telegram"


def send(message):
    for subscriber_id in _subscribers:
        _bot.send_message(subscriber_id, message)


def poll():
    global _bot
    logging.debug('polling telegram messages')
    try:
        _bot.polling(none_stop=False, timeout=3)
    except (KeyboardInterrupt, SystemExit):
        logging.debug('telegram')


def save():
    pickle.dump(_subscribers, open(TELEGRAM_DB, 'wb'))
