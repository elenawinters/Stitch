from flask import request, redirect, url_for
from ...api import app, loop, base
from core.logger import log
from dateutil import parser
from core import time, json
from data.data import data
import datetime


rate = datetime.datetime.utcnow()
prefixes = {}


@app.route("/discord/prefix/<ident>", methods=['GET', 'POST'])
def prefix(ident=None):
    if request.method == 'POST':
        data.base['cache'].upsert(dict(platform='discord', type='prefix', id=ident, data=request.json['prefix']), ['id'])
        refresh_prefixes(True)
    else:
        refresh_prefixes()

    return base(prefixes.get(ident, json.orm['discord']['prefixes']['default']), request)


def refresh_prefixes(force: bool = False):
    global rate, prefixes
    if force or time.misc.diff(rate, datetime.datetime.utcnow()).seconds >= 1800 or len(prefixes) == 0:
        [prefixes.update({x['id']: x['data']}) for x in data.base['cache'].find(platform='discord', type='prefix')]
        rate = datetime.datetime.utcnow()
