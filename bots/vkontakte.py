from vk_api import VkApi
import logging

# SUBSCRIBERS_DB = "vkontakte.data"
_api = None
_group_id = None


def init(config):
    global _api
    global _group_id

    logging.info('%s initialization' % get_name())
    vk_session = VkApi(app_id=config['app_id'], client_secret=config['client_secret'])

    vk_session.server_auth()
    _api = vk_session.get_api()
    _group_id = config['group_id']


def send(message):
    assert(_api)
    res = _api.wall.post(owner_id=-_group_id, from_group=1, message=message)

    logging.debug(str(res))


def poll():
    pass


def save():
    pass


def get_name():
    return "vkontakte"
