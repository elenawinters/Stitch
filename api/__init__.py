from .web.api import app, logger
from core import json
import threading
import importlib


class Initialize():
    def __init__(self):
        self.threads = [threading.Thread(target=self.run, daemon=True, name='API')]
        [thread.start() for thread in self.threads]

    def run(self):
        try:  # Start Web API
            app.run(host=json.orm['api']['host'], port=json.orm['api']['port'])
        except Exception as exc:
            logger.log.exception(exc)
