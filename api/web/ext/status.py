from flask import request, redirect, url_for
from ..api import app, loop, base
from core.logger import log
from dateutil import parser
from core import time, json
import datetime

uptime = datetime.datetime.utcnow()
data = {
    'discord': {}
}


@app.route("/uptime/", methods=['GET', 'POST'])
def uptime():
    if request.method == 'POST':
        global uptime
        uptime = parser.parse(request.json['uptime'])
    diff = {'uptime': time.readable.timedelta(time.misc.diff(uptime, datetime.datetime.utcnow()))}
    return base(diff, request)


@app.route("/stat/", methods=['GET', 'POST'])
def status():
    global data
    if request.method == 'POST':
        json.internal.merge(data, request.json)

    data.update({'uptime': time.readable.timedelta(time.misc.diff(uptime, datetime.datetime.utcnow()))})
    return base(data, request)
