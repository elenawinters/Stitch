from core.logger import log, trace, json
from discord.ext import commands
from data.data import data
from .tools import tls
import core.web


def is_banned():
    async def predicate(ctx):
        ban = data.base['bans'].find_one(id=ctx.author.id)
        if ban:
            raise tls.Exceptions.GlobalBanException
        return not False  # Returns True so that the program can continue if not banned
    return commands.check(predicate)


def manager():
    async def predicate(ctx):
        if ctx.auhor.id in list(managers()):
            return True
    return commands.check(predicate)


async def managers():
    host = json.orm['api']
    try:
        r = await core.web.Client(f"http://{host['host']}:{host['port']}/managers").async_get()
        return r.json()
    except Exception:
        return []


def assitant():
    async def predicate(ctx):
        assistants = await core.web.Client(f"http://{host['host']}:{host['port']}/assistants").async_get().json()
        if ctx.auhor.id in list(assistants()):
            return True
    return commands.check(predicate)


async def assistants():
    host = json.orm['api']
    try:
        r = await core.web.Client(f"http://{host['host']}:{host['port']}/assistants").async_get()
        return r.json()
    except Exception:
        return []
