from .api import app, logger
from core import json
import threading
import importlib


class Initialize():
    def __init__(self):
        self.threads = [threading.Thread(target=self.run, daemon=True, name='API')]
        [thread.start() for thread in self.threads]

    def run(self):
        try:  # Start Web API
            # from core.queue import queue
            # # from data.data import data
            # while True:
            #     if not isinstance(item := queue.listen(rate=60), type(None)):
            #         queue.send(item['sender'], item['message'])
            # # logger.log.debug(item)
            # _pre = data.base['cache'].find_one(platform=item['message'][0], type='prefix', id=item['message'][1])
            # if _pre:
            #     queue.send(item['sender'], json.orm['discord']['prefixes']['default'])
            # else:
            #     queue.send(item['sender'], _pre['data'])

            app.run(host=json.orm['api']['host'], port=json.orm['api']['port'])
        except Exception as exc:
            logger.log.exception(exc)
