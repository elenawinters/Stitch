from core.defaults import defaults
from core.bot.funcs import log
from core.bot.time import *
from core.bot import tools
from core import json
from data import data
import datetime
import discord
import os


def startup():
    do_setup()
    json.json()
    reset_logs()


def do_setup():
    if not json.external.exists():
        json.external.write(defaults.settings)
        json.json()
        token = input(f"[{time.Now.unix()}] What is the main bot's login token? ")
        json.json.orm['tokens'] = [tools.crypt(token)]


def reset_logs(force=False):
    pass
    # logs = json.json.orm['settings']['logging']['file']
    # if logs['override'] or force:
    #     if json.external.exists(logs['file']):
    #         open(logs['file'], 'w').close()
    #         log(f'{trace.black}{trace.white.b.s}> Cleared the log file. {trace.time}{time.readable.on(trace.black)}{trace.black}.')
