from flask import Flask, jsonify, render_template, make_response, send_from_directory
from core import logger, util, json
from threading import Thread
import importlib
import asyncio
import sys
import os


# https://gist.github.com/jerblack/735b9953ba1ab6234abb43174210d356
sys.modules['flask.cli'].show_server_banner = lambda *x: None  # Hide warning message

loop = asyncio.get_event_loop()  # Define loop so that things that require it can use it
app = Flask('stitch-api')
app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=False,  # This is handled by base() now, and not necessary
    ENV='production'
)


@app.route('/favicon.ico')  # TODO: Find or create new icon
def favicon():  # Knit by Aenne Brielmann from the Noun Project
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
    # return send_from_directory(os.path.join(os.getcwd(), 'assets'),
    #                            'favicon.ico', mimetype='image/vnd.microsoft.icon')


# https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.useragents.UserAgent.browser
def base(render, request=None):  # Dark theme JSON in browsers
    if request is None or request.user_agent.browser is None:
        return jsonify(render)
    else:  # base.html is located in the templates folder. You can modify it there
        return render_template('base.html', render=json.internal.dumps(render, True))


imports = util.imports(util.path(__file__), 'ext')
abspath = os.path.abspath('')


for x in imports:
    try:
        importlib.import_module(x, abspath)
        # logger.log.debug(f'Loaded {x}')
    except Exception as exc:
        logger.log.error(exc)
