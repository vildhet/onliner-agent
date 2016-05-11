#!/usr/bin/env python3

import requests
import argparse
import json
import logging
import copy
import time
import pickle

_bots = []
APARTMENTS_DB = 'aparments.data'


def init_bots(config):
    logging.info('init all bots')
    from bots import telegram
    _bots.append(telegram)

    for bot in _bots:
        bot.init(config['bots'][bot.get_name()])


def send_announce(message):
    logging.info('sending announce message via all bots: \"%s\"' % message)

    for bot in _bots:
        bot.send(message)


def poll_bots():
    for bot in _bots:
        bot.poll()


def save_bots_states():
    for bot in _bots:
        bot.save()


def poll_site(config):
    def save(data):
        pickle.dump(data, open(APARTMENTS_DB, 'wb'))

    def load():
        try:
            return pickle.load(open(APARTMENTS_DB, 'rb'))
        except (IOError, EOFError):
            return []

    params = copy.deepcopy(config['request'])
    params['page'] = 1
    h_apparments = load()

    while True:
        r = requests.get(config['api_url'], params)

        if r.status_code == 200:
            apartments = r.json()['apartments']
            if len(apartments) == 0:
                break

            for a in apartments:
                h_a = next((h_a for h_a in h_apparments if h_a['id'] == a['id']), None)
                if h_a is None:
                    h_apparments.append(a)
                    send_announce('{photo}, {created_at}, "{location[address]}", {url}, #{id}'.format(**a))
        else:
            logging.warn('invalid response code: %d' % r.status_code)
            break

        params['page'] += 1

    save(h_apparments)


def main(options):
    config = json.load(open(options.config, 'r'))
    init_bots(config)

    try:
        while True:
            poll_site(config)
            poll_bots()
            time.sleep(60.0)
    except (KeyboardInterrupt):
        logging.info('interrupting service')
        save_bots_states()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default="config.json")
    options = parser.parse_args()
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    main(options)
