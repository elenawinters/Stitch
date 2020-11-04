import discord
from discord.ext import commands
from ...core.tools import tls
from core.logger import log
from core import time
import datetime
# import core.checks


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['userinfo'])
    async def whois(self, ctx, *, user):
        try:
            user = await commands.MemberConverter().convert(ctx=ctx, argument=user)
        except commands.BadArgument:
            try:
                user = await commands.UserConverter().convert(ctx=ctx, argument=user)
            except commands.BadArgument:
                try:
                    user = tls.search(user, self.bot.users)[0]
                except IndexError:
                    user = None
        # nicknames = []
        try:
            async with ctx.typing():
                display = [y.nick for x in self.bot.guilds for y in x.members if y.id == user.id if y.nick]
                servers = [x for x in self.bot.guilds for y in x.members if y.id == user.id]

            display = ', '.join(tls.remove_duplicates(display))
            if display == '':
                display = None
            age = time.readable.timedelta(time.misc.diff(user.created_at, datetime.datetime.utcnow()))
            embed = tls.Embed(ctx, description=f'Information about {user.mention} **({user})**', timestamp=True)
            embed.add_field(name='Identifier:', value=f'`{user.id}`', inline=True)
            embed.add_field(name='Created At:', value=f'`{user.created_at}`', inline=True)
            embed.add_field(name=f'Account Age:', value=f'```{age}```', inline=False)
            embed.add_field(name=f'Known Nicknames:', value=f'```{display}```', inline=False)
            if len(servers) == 1:
                embed.set_footer(icon_url=user.avatar_url, text=f'In {len(servers)} guild (that can be seen)')
            else:
                embed.set_footer(icon_url=user.avatar_url, text=f'In {len(servers)} guilds (that can be seen)')

            await ctx.send(embed=embed)
        except Exception as exc:
            log.exception(exc)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def cogs(self, ctx):
        """Display all loaded cogs"""
        color = get_color(ctx)
        unique_cogs = set({})
        for x in self.bot.commands:
            unique_cogs.add(x.cog_name)
        cogs = {}
        for x in unique_cogs:
            cogs[x] = []
        for x in self.bot.commands:
            cogs[x.cog_name].append(x.name)
        listeners = []
        for y in self.bot.cogs:  # listeners
            cog = self.bot.get_cog(y)
            for name, func in cog.get_listeners():
                listeners.append(name)
        embed = tls.Embed(ctx, description=f'Here are the currently loaded cogs: ({len(self.bot.commands)} commands, {len(self.bot.cogs)}/{len(self.bot.extensions)} cogs, {len(listeners)} listeners)')
        for k, v in sorted(cogs.items()):
            for x in sorted(v):
                embed.add_field(name=f'cogs.{k}', value=x, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='command', aliases=['comm', 'commands', 'com'], hidden=True)
    @commands.is_owner()
    async def comm(self, ctx, name=None):
        if name is not None:
            x = tls.Command.fetch(self, name)
            if x:
                embed = tls.Embed(ctx, description=f'Command info for **.{x}**')
                embed.add_field(name='Cog:', value=x.cog_name.capitalize(), inline=True)
                embed.add_field(name='Command:', value=x.name.capitalize(), inline=True)
                embed.add_field(name='Name:', value=x.qualified_name.capitalize(), inline=True)
                embed.add_field(name='Hidden:', value=x.hidden, inline=True)
                embed.add_field(name='Enabled:', value=x.enabled, inline=True)
                embed.add_field(name='Parent:', value=x.parent, inline=True)
                if x.help is not None:  # Show help if exists
                    embed.add_field(name='Help:', value=x.help, inline=False)
                if bool(x.aliases) is True:  # Show aliases if any exist
                    embed.add_field(name='Aliases:', value=x.aliases, inline=False)
                if bool(x.checks) is True:  # Show checks if any exist
                    embed.add_field(name='Checks:', value=x.checks, inline=False)
                await ctx.send(embed=embed)

            if not x:
                embed = tls.Embed(ctx, description='No command found.')
                await ctx.send(embed=embed)

        else:
            await tls.Command.execute(self, ctx, 'status')

    @commands.command(aliases=['aliases', 'al'], hidden=True)
    async def alias(self, ctx, name=None):
        if name is not None:
            x = tls.Command.fetch(self, name)
            if x:
                embed = tls.Embed(ctx, description=f'Alias info for **.{x}**')
                # embed = tls.Embed(ctx)
                embed.add_field(name='Command:', value=x.name.capitalize(), inline=True)
                embed.add_field(name='Aliases:', value=x.aliases, inline=True)
                await ctx.send(embed=embed)
        else:
            embed = tls.Embed(ctx, description=f'{name} was not found.')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def dump(self, ctx):  # Dump every command available
        await ctx.send("**Commands:**\n" + ''.join([str(x) + '\n' for x in tls.remove_duplicates([y for y in self.bot.walk_commands()])]))


def setup(bot):
    bot.add_cog(Core(bot))
