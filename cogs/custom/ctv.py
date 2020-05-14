import discord
from discord.ext import commands
from core.bot import perms
from core.color import trace
from core.logger import log
from core import json
from data.data import data
from core.bot.tools import tls
import asyncio
import aiohttp
import ast
from core.bot.tools import crypt
import session
test = True
header = {
        'Client-ID': crypt(json.json.orm['secure']['extractors']['twitch']),
        'Accept': 'application/vnd.twitchtv.v5+json'
}
do_loop = True
looping = False
last_live = 0


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @perms.is_admin()
    async def ctv(self, ctx):
        if not ctx.invoked_subcommand:
            # Todo: Implement announcements
            # ctv_live = await is_online()
            # await assignment_checks(self, ctv_live)
            # for x in ctx.guild.members:
            #     for z in x.activities:
            #         if z.type == discord.ActivityType.streaming:
            #             _id = await name_to_id(z.twitch_name)
            #             data.base['ctv_users'].upsert(dict(userid=_id, discorduid=x.id), ['discorduid'])
            #             print(f'Debug | {x.name}: {z.twitch_name} / {_id}, {z.url}')
            pass

    @ctv.command()
    @commands.is_owner()
    async def find(self, ctx, name):
        print(await name_to_id(name))

    @ctv.command(name='reset')
    @commands.is_owner()
    async def do_reset(self, ctx):
        global do_loop
        do_loop = False
        count = 0
        while looping:
            count += 1
            if count >= 6:
                break
            await asyncio.sleep(10)
        if count <= 6:
            do_loop = True
            global now
            now = []
            global past
            past = []
            await live_loop(self)

    @commands.Cog.listener()
    async def on_member_update(self, before, member):
        global last_live
        for x in member.activities:
            if x.type == discord.ActivityType.streaming:
                streaming = False
                for z in before.activities:
                    if z.type == discord.ActivityType.streaming:
                        streaming = True
                        break
                if not streaming:  # If you just went live, this runs
                    if member.id != last_live:
                        last_live = member.id
                        _id = data.base['ctv_users'].find_one(discorduid=member.id)
                        try:
                            _id = _id['userid']
                        except Exception:
                            pass
                        if not _id:
                            _id = await name_to_id(x.twitch_name)
                            data.base['ctv_users'].upsert(dict(userid=_id, discorduid=member.id), ['discorduid'])
                        if test:
                            log.debug(f'{trace.alert}CTV | {member.name}: {x.twitch_name} / {_id}, {x.url}')
                        break
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        if not looping:
            await find_online_users(self)
            await live_loop(self)


def setup(bot):
    bot.add_cog(Custom(bot))


async def find_online_users(self):
    live = []
    for guild in self.bot.guilds:
        for member in guild.members:
            for x in member.activities:
                if x.type == discord.ActivityType.streaming:
                    new = {'user': member.id, 'twitch': x.twitch_name}
                    if new not in live:
                        live.append(new)

    for x in live:
        _id = data.base['ctv_users'].find_one(discorduid=x['user'])
        if not _id:
            _id = await name_to_id(x['twitch'])
            data.base['ctv_users'].upsert(dict(userid=_id, discorduid=x['user']), ['discorduid'])
        # _id = await name_to_id(x['twitch'])
        # data.base['ctv_users'].upsert(dict(userid=_id, discorduid=x['user']), ['discorduid'])


async def name_to_id(_name):
    url = "https://api.twitch.tv/kraken/users?login=" + _name
    try:
        async with session.session.get(url, headers=header) as r:
            _data = await r.json(encoding='utf-8')
    except Exception:
        pass
    try:
        if r.status == 200:
            if _data['users']:
                return _data['users'][0]['_id']
    except Exception:
        pass
    return False


async def is_online():
    _id = []
    for x in data.base['ctv_users']:
        _id.append(x['userid'])
    _id = ','.join([str(elem) for elem in _id])
    url = "https://api.twitch.tv/kraken/streams/?channel=" + _id
    try:
        async with session.session.get(url, headers=header) as r:
            _data = await r.json(encoding='utf-8')
    except Exception:
        pass
    try:
        if r.status == 200:
            if _data["streams"]:
                return _data
    except Exception:
        pass
    return None


async def get_stream(ctv_user):
    url = "https://api.twitch.tv/kraken/stream/" + ctv_user
    try:
        async with session.session.get(url, headers=header) as r:
            _data = await r.json(encoding='utf-8')
    except Exception:
        pass
    try:
        if r.status == 200:
            if _data["stream"]:
                return _data
    except Exception:
        pass
    return False


async def live_loop(self):
    await reset(self)
    log.debug('CTV Loop Started')
    # if test:
    #     log.debug('CTV Loop Started')
    from cogs.core.system import lockdown
    global looping
    while not lockdown and do_loop:
        from cogs.core.system import lockdown
        if lockdown:
            break
        looping = True
        try:
            info = await is_online()
            if info:
                # print(info)
                global past
                past = now.copy()
                now.clear()
                for x in info['streams']:  # Add userID to memory
                    now.append(x['channel']['_id'])
                # if past:  # If has past history data, continue
                if True:
                    # print(info)
                    for x in now:  # Compare. If not in memory previously, it's new
                        if x not in past:
                            await on_live(self, x)
                    for x in past:  # Compare. If not in memory anymore, went offline
                        if x not in now:
                            await on_offline(self, x)
        except Exception as err:
            log.error(err)
        await asyncio.sleep(10)
    looping = False
    log.error('CTV Loop Stopped')
    # if test:
    #     log.error('CTV Loop Stopped')

now = []
past = []


async def on_live(self, ctv_channel):
    did = data.base['ctv_users'].find_one(userid=ctv_channel)
    if did:
        guilds = get_guilds(self, did['discorduid'])
        # log.debug(f'CTV Online: {guilds}')
        for x in guilds:
            gid = data.base['ctv_guilds'].find_one(guild=x.id)
            if gid:
                give_roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['give_roles'])]
                has_roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['has_roles'])]

                member = x.get_member(did['discorduid'])
                if [y for y in member.roles for x in has_roles if y.id == x.id]:
                    await member.add_roles(*give_roles)


async def on_offline(self, ctv_channel):
    did = data.base['ctv_users'].find_one(userid=ctv_channel)
    if did:
        guilds = get_guilds(self, did['discorduid'])
        # log.debug(f'CTV Offline: {guilds}')
        for x in guilds:
            gid = data.base['ctv_guilds'].find_one(guild=x.id)
            if gid:
                give_roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['give_roles'])]
                has_roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['has_roles'])]

                member = x.get_member(did['discorduid'])
                if [y for y in member.roles for x in has_roles if y.id == x.id]:
                    await member.remove_roles(*give_roles)


def get_guilds(self, did):
    return [x for x in self.bot.guilds for y in x.members if y.id == did]
    # guilds = []
    #
    # for x in self.bot.guilds:
    #     for y in x.members:
    #         if y.id == did:
    #             guilds.append(x)
    # return guilds


async def reset(self):
    try:
        for x in self.bot.guilds:
            gid = data.base['ctv_guilds'].find_one(guild=x.id)
            if gid:
                for m in x.members:
                    roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['give_roles'])]
                    if [y for y in m.roles for x in roles if y.id == x.id]:
                        await m.remove_roles(*roles)

    except Exception as err:
        import traceback
        import random
        random.seed(traceback.format_exc())
        number = random.randint(10000, 99999)
        log.exception(f'Code #{number}', exc_info=err)
        # log.error(f'Error occurred in ctv.reset. code #{number}')
        # log.exception(err)
