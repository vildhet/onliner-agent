from vk_api import VkApi
import logging
from .base import BaseBot


class VkBot(BaseBot):
    def __init__(self, config, name="vkontakte"):
        super(VkBot, self).__init__(config, name)
        logging.info('%s initialization' % self.name)
        vk_session = VkApi(app_id=config['app_id'], client_secret=config['client_secret'])

        vk_session.server_auth()
        self.api = vk_session.get_api()
        self.group_id = config['group_id']

    def send(self, message):
        res = self.api.wall.post(owner_id=-self.group_id, from_group=1, message=message)
        logging.debug(str(res))

    def save_state(self):
        pass

    def poll(self):
        pass
