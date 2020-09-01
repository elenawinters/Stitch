from flask import request, redirect, url_for
from ..api import app, loop, base
from core.logger import log
import datetime

data = {}


@app.route("/stat/post/", methods=['POST'])
def stat_post():  # This is depreciated
    return redirect(url_for('stat'))


@app.route("/stat/", methods=['GET', 'POST'])
def status():
    if request.method == 'POST':
        global data
        data.update(request.json)

    return base(data, request)
