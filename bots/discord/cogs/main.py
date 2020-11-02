import discord
from discord.ext import commands
from core.logger import log, trace
from ..core import decorators
from ..core.tools import tls
from data.data import data
from core import web, json
import core.time
import traceback
import random
import sys
import ast
import re


class Stitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            await ctx.message.delete()
        except Exception:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f'{trace.cyan}> Logged in: {trace.yellow.s}{self.bot.user.name}, {trace.cyan.s}{self.bot.user.id}, {trace.magenta.s}Initiated.')

    @commands.Cog.listener()
    async def on_connect(self):
        if not self.bot.is_ready():
            log.info(f'{trace.cyan}> Logging in at {core.time.readable.at()}.')
        else:
            log.debug(f'{trace.cyan}> Connection with {trace.white}Discord{trace.cyan} achieved.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):  # COMMAND ERROR HANDLER
        if hasattr(ctx.command, 'on_error'):
            return

        elif isinstance(exc, tls.Exceptions.GlobalBanException):
            return await ctx.send(f'You are globally banned from using this bot {ctx.message.author.mention}.')

        if isinstance(exc, commands.CommandNotFound):
            delete_invalid_command = True
            if delete_invalid_command:
                com_name = list(ctx.message.content)
                if len(com_name) > 0:
                    if com_name[0] == self.bot.command_prefix(self.bot, ctx.message) and len(com_name) > 1:
                        if re.match(r'[a-zA-Z]', com_name[1]):  # IS IN COMMAND FORMAT?
                            try:
                                await ctx.message.delete()
                            except Exception:
                                pass
                            # Implement custom command support. This is per guild.
                            try:
                                ccom = ast.literal_eval(data.base['ccom'].find_one(server=ctx.guild.id)['commands'])
                            except Exception:  # Whatever the exception, move on. People who use this base might not have cComs.
                                ccom = {}
                            cname = tls.split(ctx.message.content, f'{self.bot.command_prefix(self.bot, ctx.message)}').split(' ')[0]
                            if cname not in ccom:
                                return await ctx.send(f'Sorry {ctx.message.author.mention}, but the given command does not currently exist!')

        elif isinstance(exc, commands.MissingRequiredArgument):
            return await tls.Message.respond(ctx, exc, content=f'Sorry {ctx.message.author.mention}, but you\'re missing an important argument!')

        elif isinstance(exc, commands.BadArgument):
            return await tls.Message.respond(ctx, exc, content=f'Sorry {ctx.message.author.mention}, but an argument is incorrect!')

        elif isinstance(exc, commands.DisabledCommand):
            return await ctx.send(f'Sorry {ctx.message.author.mention}, but the given command is currently disabled!')

        elif isinstance(exc, commands.MissingPermissions):
            return await ctx.send(f'Sorry {ctx.message.author.mention}, you do not have permission to run that command!')

        elif isinstance(exc, commands.NotOwner):
            return await ctx.send(f'Sorry {ctx.message.author.mention}, you do not have permission to run that command!')

        elif isinstance(exc, commands.CheckFailure):
            if ctx.guild is not None:
                return await ctx.send(f'Sorry {ctx.message.author.mention}, you do not have permission to run that command!')

        else:
            log.error(f'> {trace.red}{ctx.cog.qualified_name.capitalize()}{trace.alert} encountered {trace.red}{type(exc).__name__}'
                      f'{trace.alert} while running {trace.red}{ctx.prefix}{ctx.command}{trace.alert} with error {trace.red}{exc}')

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):  # GENERAL ERROR HANDLER
        exc = sys.exc_info()
        log.error(f'> {trace.red}{event.capitalize()}{trace.alert} encountered {trace.red}'
                  f'{exc[0].__name__}{trace.alert} with message {trace.red}{exc[1]}')
        log.exception(**tls.Traceback(exc).code())

    @commands.command()
    @commands.guild_only()
    @decorators.permissions(3)
    async def prefix(self, ctx, prefix):
        form = dict(platform='discord', type='prefix', id=ctx.guild.id)
        if self.bot.command_prefix(self.bot, ctx.message) == prefix: return
        if json.orm['discord']['prefixes']['default'] == prefix:
            data.base['cache'].delete(**form)
            embed = tls.Embed(ctx, title='Deleted guld prefix', description=f'Default Prefix: `{prefix}`', timestamp=True)
        else:
            data.base['cache'].upsert(dict(**form, data=prefix), ['id'])
            embed = tls.Embed(ctx, title='Updated guld prefix', description=f'New Prefix: `{prefix}`', timestamp=True)

        embed.set_author(name=ctx.author.nick or ctx.author.name, icon_url=ctx.author.avatar_url, url=f'https://discord.com/users/{ctx.author.id}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stitch(bot))
