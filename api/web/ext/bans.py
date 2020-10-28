from ..api import app, loop, base
from core.logger import log
from core import time, json
from data.data import data
from flask import request
import datetime

rate = datetime.datetime.utcnow()
first = True
bans = {}


@app.route("/bans/assist")
def ban_assistants():
    json.orm['permissions']
    f = 'application/api/ext/ban_assist.json'
    if not json.external.exists():
        json.external.write([], files=files)
    assists = json.external.loads(files=files)
    return base(assists, request)


@app.route("/bans/list")  # Use this to prevent the database blocking
def ban_list():
    global rate
    global bans
    global first
    if time.misc.diff(rate, datetime.datetime.utcnow()).seconds >= 10 or first:
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
