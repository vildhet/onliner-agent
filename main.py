#!/usr/bin/env python3

import requests
import argparse
import json
import logging
import copy
import time


_bots = []
APARTMENTS_DB = 'aparments.json'


def init_bots(config):
    from bots import telegram
    _bots = [telegram]

    for bot in _bots:
        bot.init(config['bots'][bot.get_name()])


def send_announce(message):
    for bot in _bots:
        bot.send(message)


def poll_bots():
    for bot in _bots:
        bot.poll()


def poll_site(config):
    def save(data):
        json.dump(data, open(APARTMENTS_DB, 'w'))

    def load():
        try:
            return json.load(open(APARTMENTS_DB, 'r'))
        except IOError:
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
                    send_announce('#{id},"{location[address]}", {created_at}, {url}, {photo}'.format(**a))
        else:
            logging.error('invalid response code: %d' % r.status_code)
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
            time.sleep(3.000)
    except KeyboardInterrupt:
        logging.info('interrupting service')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default="config.json")
    options = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    main(options)
