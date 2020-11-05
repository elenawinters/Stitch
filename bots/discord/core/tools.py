from discord.ext import commands
from core import utils, assets
import traceback
import colorsys
import datetime
import discord
import random
import httpx
import sys
import re
import os


class DiscordTools(utils.Utils):  # Discord utils
    def __init__(cls):  # inherit core.utils
        super().__init__()

    class Message:
        @classmethod
        def base(cls, err, url=discord.Embed.Empty):
            embed = tls.Embed(description=f'{err}', colour=discord.Colour.dark_red(), timestamp=True)
            embed.set_author(name=f'{type(err).__name__}', url=url, icon_url=assets.Discord.error)
            return embed

        @classmethod
        async def respond(cls, ctx, err, url=discord.Embed.Empty, content=None):
            await ctx.send(content=content, embed=cls.base(err, url=url))

        @classmethod
        async def modify(cls, msg, err, url=discord.Embed.Empty, content=None):
            await msg.edit(content=content, embed=cls.base(err, url=url))

        @classmethod
        def not_ready(cls):
            return tls.Embed(description='This action could not be completed because the bot is not ready.',
                             colour=discord.Colour.dark_grey())

    class Command:
        @classmethod
        async def execute(cls, self, ctx, name):
            for x in self.bot.commands:
                if x.name.lower() == name.lower():
                    await x.callback(self, ctx)
                    break

        @classmethod
        def fetch(cls, self, name):
            for x in self.bot.commands:
                if x.name.lower() == name.lower():
                    return x
                if name.lower() in x.aliases:
                    return x
            return None

    class Cog:
        @classmethod
        def fetch(cls, self, name):
            for _name, _cog in self.bot.cogs.items():
                if _name.lower() == name.lower():
                    return _cog
            return None

    class Voice:
        def __init__(self, ctx):
            self.ctx = ctx

        def clients(self):
            return [x.voice_client for x in self.ctx.bot.guilds if x.voice_client is not None]

        async def disconnect(self):
            for x in tls.Voice.clients(self):
                try:
                    await x.disconnect(force=True)
                except Exception:
                    pass

    class Activity:
        @classmethod
        def from_dict(cls, data):
            activity = discord.Activity()
            activity.url = data.get('url', None)
            activity.application_id = data.get('application_id', None)
            activity.assets = data.get('assets', None)
            activity.details = data.get('details', None)
            activity.flags = data.get('flags', None)
            activity.name = data.get('name', None)
            activity.party = data.get('party', None)
            activity.session_id = data.get('session_id', None)
            activity.state = data.get('state', None)
            activity.sync_id = data.get('sync_id', None)
            activity.timestamps = data.get('timestamps', None)
            activity.type = data.get('type', 0)
            return activity

        @classmethod
        async def preset(cls, bot):
            from core import json
            status = json.orm['discord']['presence'].get(str(bot.user.id), 'default').get('status', json.orm['discord']['presence']['default']['status'])
            activity = tls.Activity.from_dict(json.orm['discord']['presence'].get(str(bot.user.id), 'default').get('activity'))
            await bot.change_presence(activity=activity, status=getattr(discord.Status, status, 'online'))
            return activity, status

        @classmethod
        async def refresh(cls, bot):
            return await cls.preset(bot)

    class Users:
        @classmethod
        def nicknames(cls, self):
            nicknames = {}
            for x in self.bot.users:
                nicknames[x.id] = []
            # print(nicknames)
            for x in self.bot.guilds:
                for y in x.members:
                    if y.nick:
                        nicknames[y.id].append(y.nick)
            # for x in nicknames.copy():
            #     print('Cycle')
            #     if not nicknames[x]:
            #         print('True')
            #         nicknames.pop(x, None)
            # for x in nicknames:
            #     print(nicknames[x])
            # print(nicknames)
            return nicknames

    class Embed:
        def __new__(cls, ctx=None, **kwargs):
            color = kwargs.get('colour', DiscordTools().Color.get_color(ctx))
            title = kwargs.get('title', discord.Embed.Empty)
            _type = kwargs.get('type', 'rich')
            url = kwargs.get('url', discord.Embed.Empty)
            description = kwargs.get('description', discord.Embed.Empty)
            timestamp = kwargs.pop('timestamp', False)
            if timestamp is True:
                embed = discord.Embed(title=title, type=_type, url=url, description=description, colour=color, timestamp=datetime.datetime.utcnow())
            elif timestamp is False:
                embed = discord.Embed(title=title, type=_type, url=url, description=description, colour=color)
            else:
                try:
                    show_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                except Exception:
                    show_time = timestamp
                embed = discord.Embed(title=title, type=_type, url=url, description=description, colour=color, timestamp=show_time)

            return embed

        # @classmethod  # This will be re-added eventually
        # def parse(cls, ctx, string, bot=None):  # Parse JSON to Embed
        #     if bot is None:  # R-Filter needs to be reworked. Doesn't
        #         # work in private chats, even when it really should.
        #         try:
        #             replaced = rfilterm(ctx.author, string, ctx.bot, ctx.guild.id)
        #         except Exception:
        #             replaced = string
        #     else:
        #         try:
        #             replaced = rfilterm(ctx.author, string, bot, ctx.guild.id)
        #         except Exception:
        #             try:
        #                 replaced = rfilterm(ctx, string, bot, ctx.guild.id)
        #             except Exception:
        #                 replaced = string

        #     # JSON -> Dict
        #     try:
        #         try:
        #             import ast
        #             literal = ast.literal_eval(replaced)
        #         except Exception:  # If json function fails,
        #             # it'll output the error for it instead
        #             # of the ast.literal_eval error.
        #             import json
        #             literal = json.loads(replaced)
        #     except Exception:
        #         literal = dict(string)

        #     message = None
        #     if 'embed' in literal:
        #         try:
        #             message = literal['content']
        #         except KeyError:
        #             pass
        #         literal = literal['embed']

        #     if 'timestamp' in literal:
        #         if literal['timestamp'] == '0000-00-00T00:00:00Z':
        #             literal['timestamp'] = time.Now()
        #         else:
        #             literal['timestamp'] = time.Parse.iso(literal['timestamp'])
        #     if 'color' in literal:
        #         if literal['color'] < 0:
        #             try:
        #                 literal['color'] = get_color(bot, ctx.author).value
        #             except Exception:
        #                 literal['color'] = 0

        #     embed = discord.Embed.from_dict(literal)
        #     return embed, message

    command = Command
    embed = Embed
    users = Users
    cog = Cog

    class Color:
        @classmethod
        def from_hsv(cls, h, s=100, v=100):  # Manually parse
            # The builtin method is actually broken.
            rgb = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
            r = int(round(rgb[0] * 255))
            g = int(round(rgb[1] * 255))
            b = int(round(rgb[2] * 255))
            if r < 0:
                r = 0
            if g < 0:
                g = 0
            if b < 0:
                b = 0
            color = discord.Color.from_rgb(r, g, b)
            return color

        @classmethod
        def get_color(ctx=None, other=None):  # Dumb code
            if ctx is None:
                return discord.Colour.blurple()
            else:
                try:
                    member = ctx.message.guild.get_member(ctx.bot.user.id)
                except AttributeError:
                    try:
                        member = other.guild.get_member(ctx.user.id)
                    except AttributeError:
                        member = ctx
                try:
                    color = member.top_role.color
                except AttributeError:
                    return discord.Colour.blurple()
                if color.value == discord.Colour.default().value:
                    return discord.Colour.blurple()
                else:
                    return color

    Colour = Color
    colour = Color
    color = Color

    class Exceptions:
        class GlobalBanException(commands.CheckFailure):
            pass

    exceptions = Exceptions


tls = DiscordTools()  # Define tls so we can skip having to do DiscordTools() before everything. Reee
