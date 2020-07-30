# PERMISSION CONTROLLER. THIS STORES USER PERMISSIONS.
from discord.ext import commands
from core.bot.tools import items
from data.data import data
from core.bot.funcs import log


def is_guild(guilds):
    async def predicate(ctx):
        if any(c in guilds for c in ctx.guild.id):
            return True
        else:
            return False
        # return ctx.message.channel.permissions_for(ctx.message.author).administrator
    return commands.check(predicate)


def has_perms():
    async def predicate(ctx):
        return await get_has_perms(ctx)
    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        if await ctx.bot.is_owner(ctx.message.author):
            return True
        else:
            return ctx.message.channel.permissions_for(ctx.message.author).administrator
    return commands.check(predicate)


def subcommand():
    async def predicate(ctx):
        if ctx.invoked_subcommand is None:
            return await get_has_perms(ctx)
        else:
            return True
    return commands.check(predicate)


async def is_owner(ctx):
    return await ctx.bot.is_owner(ctx.message.author)


async def get_has_perms(ctx):
    if ctx.guild is not None:
        user = data.base['perms'].find(userid=ctx.message.author.id, serverid=ctx.message.guild.id)
        perm = items(user, 'perm')
        if ctx.command.name not in perm:
            if await is_owner(ctx):
                return True
            else:
                return ctx.message.channel.permissions_for(ctx.message.author).administrator
        else:
            return True
    else:
        return False


class Perms:
    @classmethod
    def add(cls, info):
        pass

    @classmethod
    def remove(cls, info):
        pass

    def __str__(self):
        return 'list'


perms = Perms()
