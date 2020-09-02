from ..api import app, loop, base
from core.logger import log
from data.data import data
from flask import request
from core import time
import core.json
import datetime

rate = datetime.datetime.utcnow()
first = True
bans = {}


@app.route("/bans/assist")
def ban_assistants():
    f = 'application/api/ext/ban_assist.json'
    if not core.json.external.exists(f=f):
        core.json.external.write([], f=f)
    assists = core.json.external.loads(f=f)
    return base(assists, request)


@app.route("/bans/list")  # Use this to prevent the database blocking
def ban_list():
    global rate
    global bans
    global first
    if time.time.diff(rate, datetime.datetime.utcnow()).seconds >= 10 or first:
        rate = datetime.datetime.utcnow()
        bans = ban_list()
        first = False
    return base(bans, request)


def ban_list():
    b = {}
    for x in data.base['bans'].all():
        b.update({x['id']: {
            'reason': x['reason'],
            'date': x['date'],
            'by': x['by'],
        }})
    return b
