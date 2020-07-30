import discord
from discord.ext import commands
from core.color import trace
# from core.bot.funcs import *
from core.bot.funcs import extensions
from core.bot import settings
from core.bot.tools import *
from core.bot import perms
from core.bot import enums
from core.logger import log
import core.checks
exceptions = ['restart', 'reload', 'help', 'enable', 'disable', 'cogs']
lockdown = False


class Core(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # @commands.is_owner()
    # async def broadcast(self, ctx, *, msg=''):
    #     if len(msg) > 0:  # Fix/rework soon
    #         counter = 0
    #         for x in self.bot.guilds:
    #             color = get_color(x.get_member(self.bot.user.id))
    #             embed = tls.Embed(title=f'Message from {ctx.message.author.name}, owner of {self.bot.user.name}', description=f'{msg}', colour=color)
    #             if True is True:  # FOR FUTURE SETTING
    #                 # Specifically for setting a specific channel
    #                 if x.system_channel is not None:
    #                     try:
    #                         await x.system_channel.send(embed=embed)
    #                         counter += 1
    #                     except discord.errors.Forbidden:
    #                         log(f'Failed to send broadcast to {x.name}')
    #                 else:
    #                     try:
    #                         good = False
    #                         for y in x.text_channels:
    #                             await y.send(embed=embed)
    #                             counter += 1
    #                             good = True
    #                             break
    #                         if not good:
    #                             log(f'Failed to send broadcast to {x.name}')
    #                     except discord.errors.Forbidden:
    #                         log(f'Failed to send broadcast to {x.name}')
    #
    #         await ctx.send(f'Sent broadcast to {counter}/{len(self.bot.guilds)} servers.')
    #     else:
    #         await ctx.send(f'No message specified!')

    @commands.command(aliases=['refresh'])
    @commands.is_owner()  # I hate this command.
    async def reload(self, ctx, arg='silent'):
        warnings = []
        loading = []
        unloaded = []
        import time
        before = time.monotonic()
        log.info(f'{trace.red.s}> Reloading Extensions')
        loaded = []
        for x in self.bot.extensions:
            loaded.append(x)
        cogs = extensions()
        for x in cogs:
            if x in loaded:
                try:
                    self.bot.reload_extension(x)
                    if not arg == 'silent':
                        log.info(f'{trace.cyan}> Reloaded {trace.yellow.s}{x}')
                    loaded.remove(x)
                except Exception as e:
                    warnings.append(f'Failed to reload extension {x}.\n{e}')
            elif x not in loaded:
                try:
                    self.bot.load_extension(x)
                    loading.append(x)
                except Exception as e:
                    warnings.append(f'Failed to load extension {x}.\n{e}')

        for x in loaded:
            try:
                self.bot.unload_extension(x)
                unloaded.append(x)
                loaded.remove(x)
            except Exception as e:
                warnings.append(f'Failed to unload extension {x}.\n{e}')

        if not cogs:
            log.warn('No extensions were found.')
        else:
            for x in loading:
                log.warn(f'> Loaded {x}')
            for x in unloaded:
                log.error(f'> Unloaded {x}')
            for x in warnings:
                y = x.split('\n')
                log.warn(f'> {y[0]}')
                log.error(f'> {y[1]}')
            ping = round((time.monotonic() - before) * 1000)
            log.info(f'{trace.cyan}> Reloaded {trace.yellow.s}{len(self.bot.extensions)} extensions {trace.cyan}in {trace.yellow.s}{ping}ms{trace.cyan}.')
            global lockdown
            lockdown = False
            await ctx.send(f'Extensions reloaded. ({len(self.bot.extensions)}) (`{ping}ms`)')
            from core import json
            json.json()  # Reload memory
            from core.bot.login import version
            version.Discord.latest()  # Check for updates for Discord.py
            version.YouTubeDL.latest()  # Check for updates for YouTubeDL
            await tls.Activity.preset(self.bot)  # Update activity
            # activity = tls.Activity.from_dict(json.json.orm['activity'])
            # await self.bot.change_presence(activity=activity)  # Update activity

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx, *, message=None):
        if message is None:
            await ctx.send(f'{self.bot.user.name} is restarting.')
        else:
            await ctx.send(f'{self.bot.user.name} is restarting {message}.')
        log.info(f'{trace.red.s}> Manual Restart: {trace.yellow.s}{self.bot.user.name}, {trace.cyan.s}{self.bot.user.id}, {trace.magenta.s}Restarting.')
        await tls.Voice(ctx).disconnect()
        await self.bot.close()

    @commands.command(aliases=['lockdown', 'lock', 'halt'])
    @commands.is_owner()
    async def quit(self, ctx):
        for x in self.bot.commands:
            if x.name not in exceptions:
                x.enabled = False
        await tls.Voice(ctx).disconnect()
        global lockdown
        lockdown = True
        log.info(f'{trace.red.s}> Lockdown: {trace.yellow.s}{self.bot.user.name}, {trace.cyan.s}{self.bot.user.id}, {trace.magenta.s}Halted.')
        await self.bot.change_presence(status=discord.Status.do_not_disturb)
        await ctx.send(f'{self.bot.user.name} is now in lockdown.')

    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx, arg=''):
        for x in self.bot.commands:
            if x.name == arg:
                if x.name not in exceptions:
                    x.enabled = False
                    await ctx.send(f'Disabled **.{x.name}**')
                else:
                    await ctx.send(f'The command **.{x.name}** cannot be disabled.')
                break

    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, arg=''):
        for x in self.bot.commands:
            if x.name == arg:
                if not x.enabled:
                    x.enabled = True
                    await ctx.send(f'Enabled **.{x.name}**')
                break


def setup(bot):
    bot.add_cog(Core(bot))
