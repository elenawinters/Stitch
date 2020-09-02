from .api import app, logger
import threading
import core.json


class Initialize():
    def __init__(self):
        self.threads = [threading.Thread(target=self.run, daemon=True, name='API')]
        [thread.start() for thread in self.threads]

    def run(self):
        try:  # Start API
            app.run(host=core.json.orm['api']['host'], port=core.json.orm['api']['port'])
        except Exception as exc:
            logger.log.exception(exc)
