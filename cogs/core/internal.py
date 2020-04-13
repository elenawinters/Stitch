import discord
from discord.ext import commands
from func.color import trace
from func.funcs import *
from func.tools import *


class Core(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['int', 'admin', 'bot', 'system', 'info', 'debug', 'dbg'])
    @commands.is_owner()  # OWNER ONLY FOR ENTIRE GROUP
    async def internal(self, ctx):
        if not ctx.invoked_subcommand:
            com = []
            for x in self.bot.walk_commands():
                com.append(x)
            pos = len(com)
            com = remove_duplicates(com)
            log(f'{len(com)} commands (including sub-commands)')
            log(f'{pos} possible command combinations (including aliases)')
            t = tls.search(ctx.command.name, com)
            if len(t) > 0:
                log(f'Sub-commands under this command ({len(t)}):')
            for x in t:
                log(x)

    @internal.command(name='cog')
    async def get_cog(self, ctx, name):
        cog = tls.Cog.fetch(self, name)
        log(cog.qualified_name)  # print(cog)

    @internal.command(aliases=['servers'])
    async def guilds(self, ctx):  # LIST ALL GUILDS
        log(f'Number of Guilds that this bot is in: {len(self.bot.guilds)}')
        for x in self.bot.guilds:
            log(f'{x.id}: {x.name}')

    @internal.group(aliases=['members'])
    async def users(self, ctx):  # LIST ALL USERS
        if not ctx.invoked_subcommand:
            log(f'Number of Users that this bot can see: {len(self.bot.users)}')
            for x in self.bot.users:
                log(f'{x.id}: {x}')

    @users.command(aliases=['search', 'match'])
    async def find(self, ctx, *, user):
        matches = tls.search(user, self.bot.users)
        log(f'Found {len(matches)} users that match "{user}"')
        for x in matches:
            log(f'{x.id}: {x.name}#{x.discriminator}')

    @internal.command(aliases=['member'])
    async def user(self, ctx, *, arg):  # LIST ALL USERS
        user = await commands.UserConverter().convert(ctx=ctx, argument=arg)
        log(f'Viewing user: {user.id}: {user}')
        log(f'Joined: {user.created_at}')
        guilds = []
        for x in self.bot.guilds:
            if user in x.members:
                guilds.append(x)
        log(f'Number of Guilds that {user.id} is in: {len(guilds)}')
        for x in guilds:
            log(f'{x.id}: {x.name}')

    @internal.command(aliases=['server'])
    async def guild(self, ctx, guild_id):  # LIST GUILD INFO
        guild = await self.bot.fetch_guild(guild_id)
        log(f'Viewing guild: {guild.id}: {guild}')
        owner = await commands.UserConverter().convert(ctx=ctx, argument=str(guild.owner_id))
        log(f'Owner: {guild.owner_id}: {owner}')
        # log(f'Members: {len(guild.members)} members')
        # log(f'Categories: {len(guild.categories)} categories')
        # log(f'Channels: {len(guild.channels)} channels')
        log(f'Roles: {len(guild.roles)} roles')
        log(f'Emojis: {len(guild.emojis)} emojis')
        log(f'Verification Level: {guild.verification_level}')
        log(f'Content Filter: {guild.explicit_content_filter}')
        log(f'Notifications: {guild.default_notifications}')
        log(f'Voice Region: {guild.region}')
        if len(guild.features) > 0:
            log(f'Features: {len(guild.features)}')
            for x in guild.features:
                log(f'Feature: {x}')
        log(f'Created at: {guild.created_at}')

    @guild.error
    async def guild_error(self, ctx, err):
        if isinstance(err, commands.CommandInvokeError):
            log(f'Could not find guild in cache. Error message to follow.')

    @internal.command(aliases=['createinvite'])
    async def invite(self, ctx, guild_id):  # LIST ALL USERS
        guild = await self.bot.fetch_guild(guild_id)
        log(f'Getting invite for guild: {guild.id}: {guild}')
        channels = await guild.fetch_channels()
        invite = None
        for x in channels:
            if x.position == 0:
                if type(x).__name__ == 'TextChannel':
                    invite = await x.create_invite(reason='Requested by bot owner.', unique=False, temporary=False, max_age=3600, max_uses=1)
                    break
        log(f'Invite for guild {guild.id}: {invite}')

    @invite.error
    async def invite_error(self, ctx, err):
        if isinstance(err, commands.CommandInvokeError):
            if '50001' in str(err):
                log(f'Could not find guild in cache. Error message to follow.')
            elif '50013' in str(err):
                log(f'Failed to create invite for guild. Error message to follow.')

    @internal.command()
    async def commands(self, ctx):
        com = []
        for x in self.bot.walk_commands():
            com.append(x)
        pos = len(com)
        com = remove_duplicates(com)
        for x in com:
            log(x)
            # log(type(x))
        log(f'{len(com)} commands (including sub-commands)')
        log(f'{pos} possible command combinations (including aliases)')

    # @internal.command(aliases=['createinvite'])
    # async def invite(self, ctx, guild_id):
    #     from func.ext.utility import guilds
    #     x = self.bot.get_guild(guild_id)
    #     print(x)
    #     for x in self.bot.guilds:
    #         print(guilds.find_suitable_channel(x).name)
    #     # print(guilds.find_suitable_channel(ctx.bot.get_guild(guild_id)).name)
    #     # guild.system_channel.create_invite(max_age=1, max_uses=1, unique=False, reason='Requested by bot owner.')
    #     # print('> invite')
    #     # print(ctx.args)
    #     # # print(ctx.kwargs)
    #     # print(ctx.command)
    #     # print(ctx.command.parent)
    #     # print(ctx.command.parent.callback)
    #     # print(dict(ctx.command.parent.clean_params))
    #     # print(ctx.message.content)
    #     # print(ctx.invoked_subcommand)
    #     # print(ctx.subcommand_passed)
    #     # print(guild_id)
    #     # # print('here')


def setup(bot):
    bot.add_cog(Core(bot))
