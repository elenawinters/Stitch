# from os.path import dirname, basename, isfile, join, abspath
from flask import Flask, jsonify, render_template, make_response
from threading import Thread
from core import logger
import core.utils
import core.json
import importlib
import asyncio
import json
import sys
import os

flask_log = logger.logging.getLogger('werkzeug')
# flask_log.setLevel(logging.DEBUG)

# Empty handlers, and add our custom ones
flask_log.handlers = []
flask_log.addHandler(logger.stream)
flask_log.addHandler(logger.files)

# https://gist.github.com/jerblack/735b9953ba1ab6234abb43174210d356
cli = sys.modules['flask.cli']  # Hide warning message
cli.show_server_banner = lambda *x: None

loop = asyncio.get_event_loop()  # Define loop so that things that require it can use it
app = Flask(__name__)
app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=False,  # This is handled by base() now, and not necessary
    ENV='production'
)


# https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.useragents.UserAgent.browser
def base(render, request=None):  # Dark theme JSON in browsers
    if request is None or request.user_agent.browser is None:
        return jsonify(render)
    else:  # base.html is located in the templates folder. You can modify it there
        return render_template('base.html', render=json.dumps(render, indent=2, separators=(",", ":"), default=str))


# I absolutely hate this shit
abspath = os.path.abspath('')
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ext')
imports = [core.utils.Utils().split(os.path.join(root, name), f'{abspath}', 1).replace('\\', '.')[:-3]
           for root, dirs, files in os.walk(f'{path}') for name in files
           if name.endswith('.py') and not name.endswith('__init__.py')]

for x in imports:
    try:
        importlib.import_module(x, abspath)
    except Exception as exc:
        logger.log.error(exc)


class Main(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.name = 'API'
        self.start()

    def run(self):
        try:
            app.run(host=core.json.json.orm['api']['host'], port=core.json.json.orm['api']['port'])
        except Exception as exc:
            logger.log.exception(exc)
