from core.logger import log
from data.data import data
from api import app, loop
from flask import jsonify
from core.bot import time
from core import json
import datetime

rate = datetime.datetime.utcnow()
first = True
bans = {}


@app.route("/bans/assist")
def ban_assistants():
    f = 'api_ext/ban_assist.json'
    if not json.external.exists(f=f):
        json.external.write([], f=f)
    assists = json.external.loads(f=f)
    return jsonify(assists)


@app.route("/bans/list")  # Not used? Will probably switch to this when global ban list gets too big, causing blocks
def ban_list():
    global rate
    global bans
    global first
    if time.time.diff(rate, datetime.datetime.utcnow()).seconds >= 10 or first:
        rate = datetime.datetime.utcnow()
        bans = ban_list()
        first = False
    return jsonify(bans)


def ban_list():
    b = {}
    for x in data.base['bans'].all():
        b.update({x['id']: {
            'reason': x['reason'],
            'date': x['date'],
            'by': x['by'],
        }})
    return b
