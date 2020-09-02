from flask import request, redirect, url_for
from ..api import app, loop, base
from core.logger import log
import core.time
import datetime

data = {}


@app.route("/uptime/", methods=['GET', 'POST'])
def uptime():
    if request.method == 'POST':
        global data
        log.debug(request.json)
        data.update(request.json)

    return base(data, request)
