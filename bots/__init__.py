from .telegram import TelegramBot
import threading
import logging


class EventsLoop(object):
    def __init__(self, objects):
        self.objects = objects
        self.thread = None
        self.run_events_loop = None

    def loop(self):
        while self.run_events_loop:
            for o in self.objects:
                o.poll()

    def start(self):
        self.run_events_loop = True
        self.thread = threading.Thread(target=self.loop, name="bots events loop")
        self.thread.start()

    def stop(self):
        self.run_events_loop = False

        logging.debug('saving bots state')
        for o in self.objects:
            o.save_state()

        if self.thread is not None:
            logging.debug('stopping events loop')
            self.thread.join()
            logging.debug('events loop has been stopped')

        logging.debug('saving bots state')
        for o in self.objects:
            o.save_state()

    def send_announce(self, message, subscrioption=None):
        for o in self.objects:
            o.send(message, subscrioption)
