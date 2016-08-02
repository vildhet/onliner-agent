from os import path
import requests
import logging
import pickle
import copy

from .base import BasePoller


class OnlinerPoller(BasePoller):
    def __init__(self, config, storage):
        self.config = config
        self.storage = storage

    @property
    def storage_path(self):
        return path.join(self.storage, self.config['name'])

    @property
    def request_config(self):
        return copy.deepcopy(self.config['request'])

    @property
    def api_url(self):
        return self.config['api_url']

    def poll(self, announce_fn):
        def save(data):
            pickle.dump(data, open(self.storage_path, 'wb'))

        def load():
            try:
                return pickle.load(open(self.storage_path, 'rb'))
            except (IOError, EOFError):
                return []

        params = self.request_config
        params['page'] = 1
        h_apparments = load()

        while True:
            r = requests.get(self.api_url, params)

            if r.status_code == 200:
                apartments = r.json()['apartments']
                if len(apartments) == 0:
                    break

                for a in apartments:
                    h_a = next((h_a for h_a in h_apparments if h_a['id'] == a['id']), None)
                    if h_a is None:
                        h_apparments.append(a)
                        announce_fn('{photo}, USD: {price[converted][USD][amount]}, {created_at}, "{location[address]}", {url}, #{id}'.format(**a), self.config['name'])
            else:
                logging.warn('invalid response code: %d' % r.status_code)
                break

            params['page'] += 1

        save(h_apparments)
