from os.path import dirname, basename, isfile, join, abspath
from threading import Thread
from core.logger import log
from core.json import json
from flask import Flask
import importlib
import asyncio
import glob

import logging
flask_log = logging.getLogger('werkzeug')
flask_log.setLevel(logging.ERROR)

loop = asyncio.get_event_loop()
app = Flask(__name__)

api_folder = 'api_ext'
modules = glob.glob(join(f'{dirname(__file__)}\\{api_folder}', "*.py"))
imports = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
path = abspath('.')  # This works so I don't care
for x in imports:  # Automatically load api extensions
    importlib.import_module(f'{api_folder}.{x}', path)


@app.route("/")
def root():
    return 'Stitch API Root\n\n' \
           'This API exists to assist programmers in optimizing certain functions of their bot.\n' \
           'When running multiple bots, data management should be handled by the API.'.replace('\n', '<br>')


class Main(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.name = 'API'
        self.start()

    def run(self):
        try:
            app.run(host=json.orm['api']['host'], port=json.orm['api']['port'])
        except Exception as exc:
            log.exception(exc)
