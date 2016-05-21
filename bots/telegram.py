import telebot
from telebot import types
import logging
import pickle
from .base import BaseBot


HELP_MESSAGE = """/subscribe\t\t<subscription name>
/list\t\tlist available subscriptions
/status print subsription status"""


class TelegramBot(BaseBot):
    def __init__(self, config, name='telegram'):
        super(TelegramBot, self).__init__(config, name)
        self.subscribers = self.load({})

        logging.info('init %s bot' % name)
        self.bot = telebot.AsyncTeleBot(self.bot_config['token'])

        bot = self.bot
        @bot.message_handler(commands=['help'])
        def send_welcome(message):
            self.bot.reply_to(message, HELP_MESSAGE)

        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            markup = types.ReplyKeyboardMarkup(row_width=2)
            markup.add(types.KeyboardButton('/list'), types.KeyboardButton('/subscribe'))
            self.bot.reply_to(message, HELP_MESSAGE, reply_markup=markup)

        @bot.message_handler(commands=['list'])
        def send_subscriptions(message):
            self.bot.reply_to(message, str(self.list_subscriptions()))

        @bot.message_handler(commands=['subscribe'])
        def send_subscriptions(message):
            feeds = message.text.split()[1:]
            logging.info('user %d subscribed to %s' % (message.chat.id, feeds))
            self.subscribers[message.chat.id] = feeds
            self.bot.reply_to(message, "You are sucsesfully subscribed to %s" % str(feeds))

        @bot.message_handler(commands=['status'])
        def send_status(message):
            feeds = [] if message.chat.id not in self.subscribers else self.subscribers[message.chat.id]
            self.bot.reply_to(message, str(feeds))

    def send(self, message, feed=None):
        for subscriber_id, feeds in self.subscribers.items():
            if feed in feeds or (len(feeds) == 0 and feed is None):
                self.bot.send_message(subscriber_id, message)

    def poll(self):
        logging.debug('polling %s messages' % self.name)
        try:
            self.bot.polling(none_stop=False, timeout=3)
        except (KeyboardInterrupt, SystemExit):
            logging.debug("%s interrupted" % self.name)

    def save_state(self):
        self.save(self.subscribers)
