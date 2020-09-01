import discord
from discord.ext import commands
from core.bot import perms
from core.color import trace
from core.logger import log
from core import json
from data.data import data
from core.bot.tools import tls
import asyncio
import ast
from core.bot.tools import crypt
import core.web
# import httpx as requests
header = {
    'Client-ID': crypt(json.json.orm['secure']['extractors']['twitch']),
    'Accept': 'application/vnd.twitchtv.v5+json'}
rate = datetime.datetime.utcnow()
last_live = 0
bDebug = True


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def ctv(self, ctx):
        if not ctx.invoked_subcommand:
            # Todo: Implement announcements
            # # This is old code, probably wont work
            # ctv_live = await is_online()
            # await assignment_checks(self, ctv_live)
            # for x in ctx.guild.members:
            #     for z in x.activities:
            #         if z.type == discord.ActivityType.streaming:
            #             _id = await name_to_id(z.twitch_name)
            #             data.base['ctv_users'].upsert(dict(userid=_id, discorduid=x.id), ['discorduid'])
            #             print(f'Debug | {x.name}: {z.twitch_name} / {_id}, {z.url}')
            pass

    @ctv.command(enabled=False)  # Remove
    @commands.is_owner()
    async def test_debug(self, ctx):
        global test_debug
        test_debug = not test_debug

    @ctv.command(enabled=False)  # Remove
    @commands.is_owner()
    async def looping(self, ctx):
        log.debug(looping)

    @ctv.command()
    @commands.is_owner()
    async def force_start(self, ctx):
        await do_update(self)

    @ctv.command()
    @commands.is_owner()
    async def find(self, ctx, name):
        print(await name_to_id(name))

    @ctv.command(name='reset', enabled=False)
    @commands.is_owner()  # Honestly, fuck this shit. it sucks ass
    async def do_reset(self, ctx):
        # BROKEN (I think)
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
        if not member.bot:
            # do_update(self)

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
                                if _id is not False:
                                    data.base['ctv_users'].upsert(dict(userid=_id, discorduid=member.id), ['discorduid'])
                            if test:
                                log.debug(f'{trace.alert}CTV | {member.name}: {x.twitch_name} / {_id}, {x.url}')
                            break

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
            if not member.bot:
                for x in member.activities:
                    if x.type == discord.ActivityType.streaming:
                        new = {'user': member.id, 'twitch': x.twitch_name}
                        if new not in live:
                            live.append(new)

    for x in live:
        try:
            _id = data.base['ctv_users'].find_one(discorduid=x['user'])
            if not _id:
                _id = await name_to_id(x['twitch'])
                if _id is not False:
                    data.base['ctv_users'].upsert(dict(userid=_id, discorduid=x['user']), ['discorduid'])
        except Exception as exc:
            log.exception(**tls.Traceback(exc).code())
        # _id = await name_to_id(x['twitch'])
        # data.base['ctv_users'].upsert(dict(userid=_id, discorduid=x['user']), ['discorduid'])


async def name_to_id(_name):
    if _name is not None:
        host = json.json.orm['api']
        r = await core.web.Client(f"http://{host['host']}:{host['port']}/ctv/id/{_name}").async_get()
        return r.json()
    return False


async def is_online():
    host = json.json.orm['api']
    r = await core.web.Client(f"http://{host['host']}:{host['port']}/ctv/online").async_get()
    return r.json()


async def do_update(self):
    global rate
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
        except Exception as exc:
            log.exception(**tls.Traceback(exc).code())


# async def live_loop(self):  # FUCK THIS FUCKING LOOP YOU FUCKING CUNT
#     await reset(self)
#     log.debug('CTV Loop Started')
#     # if test:
#     #     log.debug('CTV Loop Started')
#     from cogs.core.system import lockdown
#     global looping
#     while not lockdown and do_loop:
#         if test_debug:
#             log.debug(f'{self.bot.user.name} is looping')
#         from cogs.core.system import lockdown
#         if lockdown:
#             break
#         looping = True
#         try:
#             info = await is_online()
#             if info:
#                 # print(info)
#                 global past
#                 past = now.copy()
#                 now.clear()
#                 for x in info['streams']:  # Add userID to memory
#                     now.append(x['channel']['_id'])
#                 # if past:  # If has past history data, continue
#                 if True:
#                     # print(info)
#                     for x in now:  # Compare. If not in memory previously, it's new
#                         if x not in past:
#                             await on_live(self, x)
#                     for x in past:  # Compare. If not in memory anymore, went offline
#                         if x not in now:
#                             await on_offline(self, x)
#         except Exception as err:
#             log.exception(err)
#         await asyncio.sleep(10)
#     looping = False
#     log.error('CTV Loop Stopped')
#     # if test:
#     #     log.error('CTV Loop Stopped')

now = []
past = []


async def on_live(self, ctv_channel):
    did = data.base['ctv_users'].find_one(userid=ctv_channel)
    if did:
        guilds = get_guilds(self, did['discorduid'])

        for x in guilds:
            gid = data.base['ctv_guilds'].find_one(guild=x.id)
            if gid:  # do some list comprehension stuff
                give_roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['give_roles'])]
                has_roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['has_roles'])]

                member = x.get_member(did['discorduid'])
                if [y for y in member.roles for x in has_roles if y.id == x.id]:
                    await member.add_roles(*give_roles)


async def on_offline(self, ctv_channel):
    did = data.base['ctv_users'].find_one(userid=ctv_channel)
    if did:
        guilds = get_guilds(self, did['discorduid'])

        for x in guilds:
            gid = data.base['ctv_guilds'].find_one(guild=x.id)
            if gid:  # do some list comprehension stuff again
                give_roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['give_roles'])]

                member = x.get_member(did['discorduid'])
                if [y for y in member.roles for x in give_roles if y.id == x.id]:
                    await member.remove_roles(*give_roles)


def get_guilds(self, did):  # More list comprehension stuff
    return [x for x in self.bot.guilds for y in x.members if y.id == did]


async def reset(self):
    try:
        for x in self.bot.guilds:
            gid = data.base['ctv_guilds'].find_one(guild=x.id)
            if gid:
                for m in x.members:
                    roles = [tls.Snowflake(r) for r in ast.literal_eval(gid['give_roles'])]
                    if [y for y in m.roles for x in roles if y.id == x.id]:
                        await m.remove_roles(*roles)

    except Exception as exc:
        log.exception(**tls.Traceback(exc).code())
        # log.error(f'Error occurred in ctv.reset. code #{number}')
        # log.exception(err)
