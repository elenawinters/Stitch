from core.logger import log, trace, json
from discord.ext import commands
from data.data import data
from .tools import tls
import core.web


def banned():
    """
        Is the user executing the command globally banned?
    """
    async def predicate(ctx):
        if data.base['bans'].find_one(id=ctx.author.id):
            raise tls.Exceptions.GlobalBanException
        return True  # Return True so that the program can continue if not banned
    return commands.check(predicate)


def permissions(level):  # 0 for manager, 1 for assistant
    """
        Level 0: Manager (root)
        Level 1: Assistant (trusted)
        Level 2: Discord Bot Owner ()
        Level 3: Server/Guild Owner ()
    """
    levels = {
        'manager': 0,
        'assistant': 1,
        'bot': 2,
        'server': 3,
        'guild': 3
    }
    if isinstance(level, str):
        try:
            level = levels[level]
        except Exception as exc:
            log.exception(exc)
            return False

    async def predicate(ctx):
        user = data.base['permissions'].find_one(uuid=ctx.author.id, platform='discord')
        if user is not None and 'level' in user and user['level'] <= level:
            return True
        elif ctx.author.id in ctx.bot.owner_ids and level == 2:
            return True
        elif hasattr(ctx, 'guild') and ctx.guild.owner_id == ctx.author.id and level == 3:
            return True
    return commands.check(predicate)
