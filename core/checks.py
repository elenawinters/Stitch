from discord.ext import commands
from core.bot.funcs import log
from data.data import data
import core.exceptions
import core.json
import core.web


def is_banned():
    async def predicate(ctx):
        ban = data.base['bans'].find_one(id=ctx.author.id)
        if ban:
            raise core.exceptions.GlobanBanExcpetion
        return not False  # Returns True so that the program can continue if not banned
    return commands.check(predicate)


def ban_assitant():
    async def predicate(ctx):
        if ctx.auhor.id in list(ban_assistants()):
            return True
    return commands.check(predicate)


async def ban_assistants():
    host = core.json.orm['api']
    try:
        r = await core.web.Client(f"http://{host['host']}:{host['port']}/bans/assist").async_get()
        return r.json()
    except Exception:
        return []

    # try:
    #     async with requests.AsyncClient() as client:
    #         r = await requests.get(url=f"http://{host['host']}:{host['port']}/bans/assist")
    #     return r
    # except requests._exceptions.ConnectTimeout:
    #     log.debug('Bans Connect Timeout')
    # except requests._exceptions.ReadTimeout:
    #     log.debug('Bans Read Timeout')
    # except Exception as exc:
    #     log.exception(exc)
    # return []
