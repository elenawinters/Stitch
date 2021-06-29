from core.logger import log, trace
from discord.ext import commands
from .core import decorators
from .core.tools import tls
from data.data import data
from core import web, json
import core.time
import threading
import discord
import time
import sys
import ast
import re
import os


class CogLoader:
    def __init__(self, client: commands.Bot):
        if not isinstance(client, commands.Bot):
            raise TypeError(f"Expected 'commands.Bot' but received {type(client)}! Unable to continue!")
        self.client = client
        self.exc = {}

    def load(self):
        self.client.remove_command('help')
        self.reload()

    def reload(self):  # https://stackoverflow.com/a/42376244/14125122
        cogs = tls.remove_duplicates(tls.imports(tls.path(__file__), 'cogs'))
        loaded = [x for x in self.client.extensions]

        for x in cogs:
            try:
                if x in loaded:
                    self.client.reload_extension(x)
                    loaded.remove(x)
                else:
                    self.client.load_extension(x)
            except Exception as e:
                e_names = str(e).split(':')  # this is jank
                if len(e_names) == 1 or not e_names[1].endswith('BotSpecificCog'):
                    self.exc.update({x: e})

        for x in self.exc:
            log.warning(f'Failed to load extension {x}')
            log.error(self.exc[x])

        count = len(self.exc)

        if count >= 1:
            log.error(f"> Failed to load {trace.yellow.s}{count}{trace.cyan} extension{'' if count == 1 else 's'}.")

        log.info(f"{trace.cyan}> Loaded {trace.yellow.s}{len(self.client.extensions)}{trace.cyan} extension"
                 f"{'' if len(self.client.extensions) == 1 else 's'}!")

        self.client.dispatch('cogs_ready')  # this is an undocumented call. This will call custom listeners with the name of 'on_cogs_ready'

    def restart(self):
        pass


class StitchEntryLoad(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        old_name = threading.current_thread().name
        new_name = f'({old_name}) {self.bot.user.name}'
        threading.current_thread().name = new_name  # new thread name
        log.debug(f'Thread "{old_name}" changed name to "{new_name}"')
        log.debug(f'{self.bot.user.name} is ready! Loading extensions!')
        CogLoader(self.bot).load()

        log.info(f'{trace.cyan}> Logged in: {trace.yellow.s}{self.bot.user.name}, {trace.cyan.s}{self.bot.user.id}, {trace.magenta.s}Initiated.')

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        try:
            await ctx.message.delete()
        except Exception:
            pass

    @commands.Cog.listener()
    async def on_connect(self):
        if not self.bot.is_ready():
            log.info(f'{trace.cyan}> Logging in at {core.time.readable.at()}.')
        else:
            log.debug(f'{trace.cyan}> Connection with {trace.white}Discord{trace.cyan} achieved.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, exc: Exception):  # COMMAND ERROR HANDLER
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
    async def on_error(self, event: str, *args, **kwargs):  # GENERAL ERROR HANDLER
        exc = sys.exc_info()
        log.error(f'> {trace.red}{event.capitalize()}{trace.alert} encountered {trace.red}'
                  f'{exc[0].__name__}{trace.alert} with message {trace.red}{exc[1]}')
        log.exception(**tls.Traceback(exc).code())

    @commands.command()
    @commands.guild_only()
    @decorators.permissions(3)
    async def prefix(self, ctx: commands.Context, prefix: str):
        form = dict(platform='discord', type='prefix', id=ctx.guild.id)
        if self.bot.command_prefix(self.bot, ctx.message) == prefix: return
        if json.orm['discord']['prefixes']['default'] == prefix:
            data.base['cache'].delete(**form)
            embed = tls.Embed(ctx, title='Deleted guild prefix', description=f'Default Prefix: `{prefix}`', timestamp=True)
        else:
            data.base['cache'].upsert(dict(**form, data=prefix), ['id'])
            embed = tls.Embed(ctx, title='Updated guild prefix', description=f'New Prefix: `{prefix}`', timestamp=True)

        embed.set_author(name=ctx.author.nick or ctx.author.name, icon_url=ctx.author.avatar_url, url=f'https://discord.com/users/{ctx.author.id}')
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(StitchEntryLoad(bot))
