from flask import jsonify, request
from core.logger import log
from api import app, loop
import datetime

data = {}


@app.route("/stat/post/", methods=['POST'])
def stat_post():
    global data
    data.update(request.json)
    return jsonify(None)


@app.route("/stat/")
def status():
    return jsonify(data)
