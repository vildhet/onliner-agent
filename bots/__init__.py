from . import telegram
import logging
import threading

_bots = []
_run_bots_events_loop = True
_events_loop_thread = None


def init(config):
    logging.info('init all bots')

    from bots import telegram, vkontakte
    _bots.append(telegram)
    # _bots.append(vkontakte)

    for bot in _bots:
        bot.init(config['bots'][bot.get_name()])


def send_announce(message):
    logging.info('sending announce message via all bots: \"%s\"' % message)

    for bot in _bots:
        bot.send(message)


def poll():
    for bot in _bots:
        bot.poll()


def save_states():
    for bot in _bots:
        bot.save()


def start():
    global _run_bots_events_loop
    global _events_loop_thread

    _run_bots_events_loop = True

    def _bots_loop():
        while _run_bots_events_loop:
            poll()

    _events_loop_thread = threading.Thread(target=_bots_loop, name="bots events loop")
    _events_loop_thread.start()

    send_announce('service is working now')


def stop():
    global _run_bots_events_loop
    _run_bots_events_loop = False
    if _events_loop_thread is not None:
        _events_loop_thread.join()

    save_states()
