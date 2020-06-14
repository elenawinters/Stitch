from core.bot.tools import crypt
from core.logger import log
from data.data import data
from api import app, loop
from core.bot import time
from flask import jsonify
from core import json
import datetime
import httpx as requests


header = {
    'Client-ID': crypt(json.json.orm['secure']['extractors']['twitch']),
    'Accept': 'application/vnd.twitchtv.v5+json'
}
rate = datetime.datetime.utcnow()
is_online_data = None
last_name_data = ''
last_name_id = 0


@app.route("/ctv/id/<name>")
def ctv_id_name(name):
    global rate
    global last_name_id
    global last_name_data
    if last_name_data != name:
        last_name_id = name_to_id(name)
        last_name_data = name
    # log.debug(is_online_data)
    return jsonify(last_name_id)


def name_to_id(name):
    url = "https://api.twitch.tv/kraken/users?login=" + name
    try:
        r = requests.get(url=url, headers=header)
        r_json = r.json()
        if r_json['users']:
            return r_json['users'][0]['_id']
    except requests._exceptions.ConnectTimeout:
        log.debug('Connect Timeout')
    except requests._exceptions.ReadTimeout:
        log.debug('Read Timeout')
    except Exception as exc:
        log.exception(exc)
    return None


@app.route("/ctv/online")
def ctv_online():
    global rate
    global is_online_data
    if time.time.diff(rate, datetime.datetime.utcnow()).seconds >= 10:
        rate = datetime.datetime.utcnow()
        is_online_data = is_online()
    return jsonify(is_online_data)


def is_online():
    _id = []
    for x in data.base['ctv_users']:
        _id.append(x['userid'])
    _id = ','.join([str(elem) for elem in _id])
    url = "https://api.twitch.tv/kraken/streams/?limit=100&channel=" + _id

    try:
        r = requests.get(url=url, headers=header)
        r_json = r.json()
        if r_json['streams']:
            return r_json
    except requests._exceptions.ConnectTimeout:
        log.debug('Connect Timeout')
    except requests._exceptions.ReadTimeout:
        log.debug('Read Timeout')
    except Exception as exc:
        log.exception(exc)
    return None
