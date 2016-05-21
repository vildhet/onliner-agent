import pickle
from os import path
import logging


class BaseBot(object):
    def __init__(self, config, name):
        self.config = config
        self.name = name

    @property
    def bot_config(self):
        return self.config['bots'][self.name]

    def list_subscriptions(self):
        return [s for s in self.config['pollers']]

    @property
    def db_path(self):
        return path.join(self.config['storage'], self.name)

    def load(self, default=None):
        try:
            return pickle.load(open(self.db_path, 'rb'))
        except (IOError, EOFError):
            return default

    def save(self, data):
        logging.debug('saving to %s' % self.db_path)
        pickle.dump(data, open(self.db_path, 'wb'))

    def save_state(self):
        raise Exception("Is not implemented yet")
