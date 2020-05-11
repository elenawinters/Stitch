from discord.ext import commands
from core.bot.time import time
from .enums import *
import colorsys
import datetime
import discord
import sys
import os


class tls:  # Short for Tools
    @classmethod
    def search(cls, find, data):
        matches = []
        for x in data:
            if find.lower() in f'{str(x).lower()}':
                matches.append(x)
        return matches

    class Snowflake:
        def __init__(self, snowflake):
            self.id = snowflake

    class Voice:
        def __init__(self, ctx):
            self.ctx = ctx

        def clients(self):
            r = []
            for x in self.ctx.bot.guilds:
                if x.voice_client is not None:
                    r.append(x.voice_client)
            return r

        async def disconnect(self):
            for x in tls.Voice.clients(self):
                try:
                    await x.disconnect(force=True)
                except:
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
            activity = tls.Activity.from_dict(json.json.orm['activity'].get(str(bot.user.id), json.json.orm['activity']['default']))
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
                except:
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


#  Replacement filter - member
def rfilterm(member, string: str, bot=None, guid=None, channel=None):
    string = string.replace('method.get.color', str(get_color(bot, member).value))
    string = string.replace('method.color', str(get_color(bot, member).value))
    string = string.replace('method.timestamp', str(datetime.datetime.utcnow()))
    string = string.replace('method.datetime', str(datetime.datetime.utcnow()))
    string = string.replace('member.avatar_url', str(member.avatar_url))
    string = string.replace('member.avatar', str(member.avatar_url))
    string = string.replace('member.name', member.name)
    string = string.replace('member.tag', str(member))
    string = string.replace('member.guild.name', str(member.guild.name))
    string = string.replace('guild.name', str(member.guild.name))
    if bot is not None:
        string = string.replace('bot.name', str(bot.user.name))
        string = string.replace('bot.avatar_url', str(bot.user.avatar_url))
        string = string.replace('bot.avatar', str(bot.user.avatar_url))
    if guid is not None:
        if bot is not None:
            guild = bot.get_guild(guid)
            if guild.icon is None:
                string = string.replace('guild.icon', DiscordAvatars.default)
            else:
                string = string.replace('guild.icon', str(guild.icon_url))
    else:
        if member.guild.icon is None:
            string = string.replace('guild.icon', DiscordAvatars.default)
        else:
            string = string.replace('guild.icon', str(member.guild.icon_url))
    return string


def split_string(string, remove, offset=0):
    return string[len(f'{remove}')+offset:]


def remove_duplicates(x: list):
    return list(dict.fromkeys(x))


def short_traceback():
    err = []
    for x in sys.exc_info():
        err.append(x)
    return f"{err[0].__name__}: {err[1]}"


def err_traceback():
    err = []
    for x in sys.exc_info():
        err.append(x)
    return err


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_color(ctx=None, other=None):
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


def get_files(path):
    output = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".py"):
                output.append(f'{root}\\{name}')

    return output


def append_cog(file, package=''):
    from core.bot import funcs
    import os  # Huge mess but it works.
    path = os.path.abspath('.')
    for root, dirs, files in os.walk(path):
        for name in files:
            if file == name:
                if name.endswith(".py"):
                    output = split_string(f'{root}\\{name}', path, offset=1).replace('\\', '.')
                    if package == '':
                        funcs.c_cogs.append(f'{output}')
                        return f'{output}'
                    else:
                        funcs.c_cogs.append(f'{package}.{output}')
                        return f'{package}.{output}'
    return None


def voice_clients(ctx):
    clients = []
    for x in ctx.bot.guilds:
        if x.voice_client is not None:
            clients.append(x.voice_client)

    return clients


def crypt(s):
    x = []
    for i in range(len(s)):
        j = ord(s[i])
        if 33 <= j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(s[i])
    return ''.join(x)


def items(r, s):
    ret = []
    for x in r:
        for k, v in x.items():
            if k == s:
                ret.append(v)
    return ret
























