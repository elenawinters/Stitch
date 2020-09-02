from .tools import get_files, split_string, tls, append_cog
from .enums import ImageURLs, LogLevel
from core.color import trace
from ..time import *
from core import json
import traceback
import discord
c_cogs = []


def extensions():
    import os
    abspath = os.path.abspath('.')
    if os.path.dirname(abspath) == 'cogs':
        path = abspath
    else:
        path = f'{abspath}\\cogs'
    files = get_files(path)
    new = []
    for x in c_cogs:
        new.append(x)
    for x in files:
        adding = split_string(x, path).replace('\\', '.')
        new.append(f'cogs{adding}')
    # new.append(append_cog('debug.py'))  # hard code debug.py into the list
    cogs = []
    for x in new:
        if x.endswith(".py"):
            other = x.replace('.py', '')
            cogs.append(other)
    return cogs


def convert(text):
    return ''.join(i for i in text if ord(i) < 128)


def remove(text):
    for x in trace.tracers:
        text = text.replace(str(x), '')
    return text


def check(level):
    logging = json.orm['settings']['logging']['file']
    if tls.Enums(LogLevel).find(level).value <= tls.Enums(LogLevel).find(logging['level']).value:
        return True
    return False


def saved():
    return tls.Enums(LogLevel).find(json.orm['settings']['logging']['file']['level']).value
