# This will manage a 30-day audit log

from core.logger import log
from ..api import app, base
from data.data import data
from flask import request

data = {}


# what is this supposed to do again?!?
@app.route("/audit/<platform>/<gate>/", methods=['GET', 'POST'])
def audit(platform: str, gate: str):
    if request.method == 'POST':
        data.update(request.json)
    return base(data, request)


# @app.route("/audit/discord/<guild>", methods=['GET', 'POST'])
# def specifics(guild):
#     if request.method == 'POST':
#         pass
#     return None


def cleanup(data):
    return NotImplementedError
