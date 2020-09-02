from discord.ext import commands
from core.utils import items
from data.data import data


def enabled(default=True):
    async def predicate(ctx):
        if ctx.guild is not None:
            enable = data.base['extensions'].find(serverid=ctx.message.guild.id, cog=ctx.command.cog_name)
            try:
                is_enabled = items(enable, 'enabled')[0]
            except IndexError:
                is_enabled = default
            if is_enabled:
                return enable
            else:
                raise commands.errors.CommandNotFound('Command not enabled by server')
        else:
            return False

    return commands.check(predicate)


def public():
    async def predicate(ctx):
        if ctx.guild is None:
            return False
        else:
            return True
    return commands.check(predicate)






