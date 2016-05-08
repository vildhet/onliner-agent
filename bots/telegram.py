import telebot
import logging


_bot = None


def init(config):
    global _bot
    logging.info('init telegram bot')
    _bot = telebot.AsyncTeleBot(config['token'])

    @_bot.message_handler(commands=['help'])
    def send_welcome(message):
        _bot.reply_to(message, "Hello I am a smart real estate agent")

    @_bot.message_handler(commands=['start'])
    def send_welcome(message):
        logging.info('client %d subscribed' % message.chat.id)
        _bot.reply_to(message, "You have subscribed to apartments news channel")


def get_name():
    return "telegram"


def send(message):
    _bot.send(message)


def poll():
    logging.debug('polling telegram messages')
    try:
        _bot.polling(block=False)
    except (KeyboardInterrupt, SystemExit):
        logging.debug('telegram ')
