from .tools import get_files, split_string, tls, append_cog
from .enums import ImageURLs, LogLevel
from core.color import trace
from .time import *
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


def log(text, level=LogLevel.calm, only_log=False):
    if check(level):
        show = time.Now.unix()
        if not only_log:
            print(f'{trace.green.s}[{show}] {text}{trace.reset}{trace.alert}')
        save(f'[LOG] [{show}] {text}', level)


def error(text, level=LogLevel.default, only_log=False):
    if check(level):
        show = time.Now.unix()
        if not only_log:
            print(f'{trace.alert}[{show}] {trace.alert}{text}{trace.reset}{trace.alert}')
        save(f'[ERR] [{show}] {text}', level)


def warn(text, level=LogLevel.default, only_log=False):
    if check(level):
        show = time.Now.unix()
        if not only_log:
            print(f'{trace.green.s}[{show}] {trace.warn}{text}{trace.reset}{trace.alert}')
        save(f'[WRN] [{show}] {text}', level)


def debug(text, level=LogLevel.debug, only_log=False):
    if check(level):
        show = time.Now.unix()
        if not only_log:
            print(f'{trace.green.s}[{show}] {text}{trace.reset}{trace.alert}')
        save(f'[DBG] [{show}] {text}', level)


dbg = debug


async def respond(ctx, err, url=discord.Embed.Empty, content=None):
    # error(f'> {traceback.format_exc()}', LogLevel.critical)
    embed = tls.Embed(description=f'{err}', colour=discord.Colour.dark_red(), timestamp=True)
    embed.set_author(name=f'{type(err).__name__}', url=url, icon_url=ImageURLs.error)
    await ctx.send(content=content, embed=embed)


def save(text, level=LogLevel.default):
    # if json.json.orm['settings']['logging']['log']:
    if True:
        text = remove(text)
        f = open('log.txt', 'a+')
        f.write(f'{convert(text)}\n')
        f.close()


def convert(text):
    return ''.join(i for i in text if ord(i) < 128)


def remove(text):
    for x in trace.tracers:
        text = text.replace(str(x), '')
    return text


def check(level):
    logging = json.json.orm['settings']['logging']['file']
    if tls.Enums(LogLevel).find(level).value <= tls.Enums(LogLevel).find(logging['level']).value:
        return True
    return False


def saved():
    return tls.Enums(LogLevel).find(json.json.orm['settings']['logging']['file']['level']).value

