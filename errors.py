import discord
from discord.ext import commands
from core.color import trace
from core.logger import log
from data.data import data
from core.bot import funcs
import traceback
import random
import sys
import ast


class Stitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):  # COMMAND ERROR HANDLER
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(exc, commands.CommandNotFound):
            delete_invalid_command = True
            if delete_invalid_command:
                com_name = list(ctx.message.content)
                if len(com_name) > 0:
                    if com_name[0] == self.bot.command_prefix and len(com_name) > 1:
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
                            cname = funcs.split_string(ctx.message.content, f'{self.bot.command_prefix}').split(' ')[0]
                            if cname not in ccom:
                                return await ctx.send(f'Sorry {ctx.message.author.mention}, but the given command does not currently exist!')

        elif isinstance(exc, commands.MissingRequiredArgument):
            return await funcs.respond(ctx, exc, content=f'Sorry {ctx.message.author.mention}, but you\'re missing an important argument!')

        elif isinstance(exc, commands.BadArgument):
            return await funcs.respond(ctx, exc, content=f'Sorry {ctx.message.author.mention}, but an argument is incorrect!')

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
        random.seed(traceback.format_exc())
        number = random.randint(10000, 99999)
        log.error(f'> {trace.red}{event.capitalize()}{trace.alert} encountered {trace.red}'
                  f'{exc[0].__name__}{trace.alert} with message {trace.red}{exc[1]}')
        log.exception(f'Code #{number}', exc_info=exc)


def setup(bot):
    bot.add_cog(Stitch(bot))
