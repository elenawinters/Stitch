import discord
import asyncio
from discord.ext import commands
from func.color import trace
from func.funcs import *
from func.enums import *
from func.tools import *
from func.defaults.setup import reset_logs
exceptions = ['restart', 'reload', 'help', 'enable', 'disable']


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='profile', hidden=True)
    @commands.is_owner()
    async def profile(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'No invoked subcommand.')

    @profile.command(name='name', hidden=True)
    @commands.is_owner()
    async def name(self, ctx, *, name):
        try:
            await self.bot.user.edit(username=name)
            await ctx.send(f'Updated bot name to "{name}"')
        except Exception as err:
            await respond(ctx, err)

    @commands.command(name='restartclear', aliases=['clearrestart', 'restartlogclear', 'logclearrestart'], hidden=True)
    @commands.is_owner()
    async def clearrestart(self, ctx):
        reset_logs(force=True)
        await tls.Command.execute(self, ctx, 'restart')

    @commands.command(name='clearlog', aliases=['logclear'], hidden=True)
    @commands.is_owner()
    async def clearlog(self, ctx):
        reset_logs(force=True)
        await ctx.send('Cleared the log file.', delete_after=5)

    @commands.group(name='log', hidden=True)
    @commands.is_owner()
    async def log(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'No invoked subcommand.')

    @log.command(name='clear', aliases=['c'], hidden=True)
    @commands.is_owner()
    async def clear(self, ctx):
        await tls.Command.execute(self, ctx, 'clearlog')

    # @log.command(name='random', aliases=['r'], hidden=True)
    # @commands.is_owner()
    # async def clear(self, ctx, iterations: int):
    #     from func.ext.enums import names
    #     import requests
    #     import random
    #     mr = names.NameURLs.middle
    #     m = requests.get(mr.value).json()['RandL']['items']
    #     for x in range(iterations):
    #         log(random.choice(m))

    @commands.group(name='voice', hidden=True)
    @commands.is_owner()
    async def voice(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'No invoked subcommand.')

    @voice.command(name='leave', hidden=True)
    @commands.is_owner()
    async def leave(self, ctx):
        await tls.Voice(ctx).disconnect()


def setup(bot):
    bot.add_cog(Owner(bot))
