from discord.ext import commands
# from core.bot.time import time
# from .enums import *
from core import utils
import traceback
import colorsys
import datetime
import discord
import random
import httpx
import sys
import re
import os


# Todo: Convert all to use self. fuck classmethods
class Tools(utils.Utils):  # Short for Tools
    class Snowflake:  # just impersonate a snowflake obj
        def __init__(self, snowflake):
            self.id = snowflake

    class Voice:
        def __init__(self, ctx):
            self.ctx = ctx

        def clients(self):
            # r = [x.voice_client for x in self.bot.guilds if x.voice_client is not None]
            r = []
            for x in self.ctx.bot.guilds:
                if x.voice_client is not None:
                    r.append(x.voice_client)
            return r

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
            activity = tls.Activity.from_dict(json.json.orm['discord']['activity'].get(str(bot.user.id), json.json.orm['discord']['activity']['default']))
            await bot.change_presence(activity=activity)

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

        # @classmethod
        # def commands(cls, self, name):
        #     pass
        #
        # @classmethod
        # def listeners(cls, self, name):
        #     pass

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
            color = kwargs.get('colour', get_color(ctx))
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

        @classmethod
        def parse(cls, ctx, string, bot=None):  # Parse JSON to Embed
            if bot is None:  # R-Filter needs to be reworked. Doesn't
                # work in private chats, even when it really should.
                try:
                    replaced = rfilterm(ctx.author, string, ctx.bot, ctx.guild.id)
                except Exception:
                    replaced = string
            else:
                try:
                    replaced = rfilterm(ctx.author, string, bot, ctx.guild.id)
                except Exception:
                    try:
                        replaced = rfilterm(ctx, string, bot, ctx.guild.id)
                    except Exception:
                        replaced = string

            # JSON -> Dict
            try:
                try:
                    import ast
                    literal = ast.literal_eval(replaced)
                except Exception:  # If json function fails,
                    # it'll output the error for it instead
                    # of the ast.literal_eval error.
                    import json
                    literal = json.loads(replaced)
            except Exception:
                literal = dict(string)

            message = None
            if 'embed' in literal:
                try:
                    message = literal['content']
                except KeyError:
                    pass
                literal = literal['embed']

            if 'timestamp' in literal:
                if literal['timestamp'] == '0000-00-00T00:00:00Z':
                    literal['timestamp'] = time.Now()
                else:
                    literal['timestamp'] = time.Parse.iso(literal['timestamp'])
            if 'color' in literal:
                if literal['color'] < 0:
                    try:
                        literal['color'] = get_color(bot, ctx.author).value
                    except Exception:
                        literal['color'] = 0

            embed = discord.Embed.from_dict(literal)
            return embed, message

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

    Colour = Color
    colour = Color
    color = Color

    class Enums:
        def __init__(self, enum):
            self.enum = enum

        def find(self, fetch):
            fetch = str(fetch).lower()
            for x in self.enum.__members__.items():
                if fetch == str(x[1].value):
                    return x[1]
                elif fetch == str(x[1]):
                    return x[1]
                elif fetch == str(x[0]):
                    return x[1]
            return self.enum.default  # Only meant to be
            # used with enums that have a default entry.
            # if no default entry, an error will be thrown.

    Avatars = DiscordAvatars


tls = Tools()
