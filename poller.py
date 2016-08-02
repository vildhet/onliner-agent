#!/usr/bin/env python3

import requests
import argparse
import json
import logging
import copy
import time
import pickle
import threading
from bots import TelegramBot, EventsLoop

from site_api import *
import os
import shutil
from os import path


def main(options):
    config = json.load(open(options.config, 'r'))

    if not path.exists(config['storage']):
        os.makedirs(config['storage'])

    pollers = [OnlinerPoller(c, config['storage']) for c in config['pollers']]

    bots = [TelegramBot(config, 'telegram')]
    ev_loop = EventsLoop(bots)
    ev_loop.start()

    try:
        while True:
            for poller in pollers:
                poller.poll(ev_loop.send_announce)

            time.sleep(60.0)
    except (KeyboardInterrupt):
        logging.info('interrupting service')
        ev_loop.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default="config.json")
    options = parser.parse_args()
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
    main(options)
