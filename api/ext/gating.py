# Honestly, this is just glorified global variables

from core.logger import log
from ..api import app, base
from flask import request

data = {}


@app.route("/gating/", methods=['GET', 'POST'])
def keywords():
    if request.method == 'POST':
        data.update(request.json)
    return base(data, request)


@app.route("/gating/<gate>/", methods=['GET', 'POST'])
def specifics(gate: str):
    if request.method == 'POST':
        data.update({gate: request.json})
    return base(data.get(gate, None), request)
