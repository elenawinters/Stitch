#
#   Developed by Elena Winters (ElenaBerry#2561), aka Tracer
#   Contributions by: Raine Bannister
#
#   This bot is used and hosted by me (Elena), for others to use.
#
#   Codename: .tls
#   Display: Purpose
#

# This is required. Settings file will be wiped if this is not here
# from core.defaults import setup
# setup.startup()  # Run startup

from core.bot.funcs import extensions
from discord.ext import commands
# from core.defaults import setup
from core.bot.login import login
from core.color import trace
from data.data import data
from core.bot.funcs import respond
from core.bot.tools import *
from core.logger import log
from core.bot import enums
from core import json
import traceback
# import colorama
import discord
import ast
# colorama.init()
# setup.startup()
client = commands.Bot(command_prefix='.')
custom_help = True
if custom_help:
    client.remove_command('help')

if __name__ == '__main__':
    log.info(f'>{trace.cyan} Starting at {time.readable.at()}.')
    # Initialize database
    log.info(f'{trace.cyan}> Initializing {trace.black.s}dataset{trace.cyan} Database.')
    try:
        data()
        log.info(f'{trace.cyan}> Initialized {trace.black.s}dataset{trace.cyan}.')
    except Exception as err:
        log.warning(f'> Failed to load {trace.black.s}dataset{trace.warn}. Please restart!')
        log.error(f'> {short_traceback()}')
        log.critical(f'> {traceback.format_exc()}')

    # Initialize extensions
    # Append cCogs
    append_cog('debug.py')

    cog_count = 0
    warnings = []
    cogs = extensions()
    # print(cogs)
    for extension in cogs:
        try:
            client.load_extension(extension)
            cog_count += 1
        except Exception as e:
            warnings.append(f'Failed to load extension {extension}\n{e}')

    if not cogs:
        log.warn('No extensions were found.')
    else:
        for x in warnings:
            y = x.split('\n')
            log.warning(f'> {y[0]}')
            log.error(f'> {y[1]}')
        if len(warnings) > 0:
            # if saved() < enums.LogLevel.error.value:
            if len(warnings) == 1:
                log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extension.')
            else:
                log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extensions.')
        log.info(f'{trace.cyan}> Loaded {trace.yellow.s}{cog_count}{trace.cyan} extensions!')


@client.event
async def on_ready():
    log.info(f'{trace.cyan}> Logged in: {trace.yellow.s}{client.user.name}, {trace.cyan.s}{client.user.id}, {trace.magenta.s}Initiated.')


@client.event
async def on_command(ctx):
    try:
        await ctx.message.delete()
    except Exception:
        pass


@client.event
async def on_command_error(ctx, exc):  # COMMAND ERROR HANDLER
    if hasattr(ctx.command, 'on_error'):
        return

    if isinstance(exc, commands.CommandNotFound):
        delete_invalid_command = True
        if delete_invalid_command:
            com_name = list(ctx.message.content)
            if len(com_name) > 0:
                if com_name[0] == client.command_prefix and len(com_name) > 1:
                    import re
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
                        cname = split_string(ctx.message.content, f'{client.command_prefix}').split(' ')[0]
                        if cname not in ccom:
                            return await ctx.send(f'Sorry {ctx.message.author.mention}, but the given command does not currently exist!')

    elif isinstance(exc, commands.MissingRequiredArgument):
        return await respond(ctx, err, content=f'Sorry {ctx.message.author.mention}, but you\'re missing an important argument!')

    elif isinstance(exc, commands.BadArgument):
        return await respond(ctx, err, content=f'Sorry {ctx.message.author.mention}, but an argument is incorrect!')

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


@client.event
async def on_error(event):  # GENERAL ERROR HANDLER
    import traceback
    import random
    exc = sys.exc_info()
    random.seed(traceback.format_exc())
    number = random.randint(10000, 99999)
    log.error(f'> {trace.red}{event.capitalize()}{trace.alert} encountered {trace.red}'
              f'{exc[0].__name__}{trace.alert} with message {trace.red}{exc[1]}')
    log.exception(f'Code #{number}', exc_info=exc)


# Login
try:
    login(client)
except Exception as err:
    log.exception(err)
