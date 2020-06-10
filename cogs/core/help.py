import discord
from discord.ext import commands
from core.bot.funcs import extensions
from core.bot.tools import *
from core.bot import perms


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
        display = []
        servers = []
        async with ctx.typing():
            for x in self.bot.guilds:
                for y in x.members:
                    if y.id == user.id:
                        servers.append(x)
                        if y.nick:
                            display.append(y.nick)
        display = remove_duplicates(display)
        display = ', '.join(display)
        if display == '':
            display = None
        age = time.readable.From.timedelta.seconds(time.diff(user.created_at, datetime.datetime.utcnow()))
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

    # @commands.command()
    # async def help(self, ctx):
    #     """Displays this help menu."""
    #     embed = tls.Embed(ctx, description='This command is a WIP. Use **.oldhelp**')
    #     await ctx.send(embed=embed)
    #     # pass

    @commands.command(hidden=True)
    async def help(self, ctx):
        """Displays the old help menu."""
        com = ctx.message.content.split(' ')
        color = get_color(ctx)
        # SORT COMMANDS
        command = []
        new = []
        for x in self.bot.commands:
            new.append(x.name)
        sortednew = sorted(new)
        for x in range(len(sortednew)):
            for y in self.bot.commands:
                if sortednew[x] == y.name:
                    if y.enabled:
                        if y.short_doc != '':
                            command.append(y)

#
#   The help command will only display commands that you have permission to
#   use, that have a description (usage is optional), and are not hidden.
#
#   Even hidden commands can have descriptions. They can by viewed by doing
#   .help [command]. This can be used/viewed regardless of permission.
#

        if len(com) == 1:
            embed = tls.Embed(ctx, description=f'Here are the commands available to you *{ctx.message.author.mention}*:')
            for x in command:
                try:
                    if not x.hidden:
                        embed.add_field(name=f'**.{x.name}**', value=f' - {x.short_doc}', inline=False)
                    # else:
                    #    if perms.help_perms(ctx):
                    #        embed.add_field(name=f'**.{x.name}**', value=f' - {x.short_doc}', inline=False)
                except Exception as e:
                    print(e)
        else:
            is_com = False
            embed = discord.Embed(colour=color)
            for x in command:
                if x.name == com[1]:
                    is_com = True
                    embed.add_field(name=f'**{x.name.capitalize()} command:**', value=f'{x.short_doc}', inline=False)
                    if x.short_doc != x.help:
                        content = x.help[len(f'{x.short_doc}'):]
                        embed.add_field(name=f'**Usage:**', value=f'{content}', inline=False)
                    break
            if is_com is False:
                embed = tls.Embed(ctx, description=f'Sorry {ctx.message.author.mention}, but no instance of that command was found.')

        await ctx.send(embed=embed)

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
        for y in self.bot.cogs: # listeners
            cog = self.bot.get_cog(y)
            for name, func in cog.get_listeners():
                listeners.append(name)
        embed = tls.Embed(ctx, description=f'Here are the currently loaded cogs: ({len(self.bot.commands)} commands, {len(self.bot.cogs)}/{len(self.bot.extensions)} cogs, {len(listeners)} listeners)')
        for k,v in sorted(cogs.items()):
            for x in sorted(v):
                embed.add_field(name=f'cogs.{k}', value=x, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='command', aliases=['comm', 'commands', 'com'],  hidden=True)
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


def setup(bot):
    bot.add_cog(Core(bot))



















    
