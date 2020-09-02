import discord
from discord.ext import commands
from core.bot import funcs
from core.bot import perms
from core.bot.tools import tls
from core.logger import log
from data.data import data
from core import time
import core.checks
import core.json
import datetime

rate = datetime.datetime.utcnow()
bDebug = True


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ban', 'hban'])
    @commands.has_permissions(ban_members=True)
    @core.checks.is_banned()  # Simple hackban
    async def hackban(self, ctx, snowflake, *, reason='User was hackbanned'):
        try:
            await ctx.guild.ban(tls.Snowflake(snowflake), delete_message_days=0, reason=reason)
            await ctx.send(f'Hackbanned <@!{snowflake}> with reason `{reason}`.')
        except discord.Forbidden as err:
            await funcs.respond(ctx, err)
        except discord.HTTPException as err:
            await funcs.respond(ctx, err)
        except Exception as err:
            log.exception(err)

    @commands.command(aliases=['gban'])
    @core.checks.is_banned()  # To globally ban an account. (complicated D: )
    @commands.check_any(commands.is_owner(), core.checks.ban_assitant())
    async def globalban(self, ctx, snowflake, *, reason='User was globally banned'):
        ban = data.base['bans'].find_one(id=snowflake)
        if not ban:  # If None, ban
            gban = dict(
                id=snowflake,
                reason=f'{reason} (Global Ban)',
                by=ctx.author.id,
                date=datetime.datetime.utcnow()
            )
            data.base['bans'].upsert(gban, ['id'])
            await ban_sweep(self)
            await ctx.send(f'<@!{ctx.author.id}> globally banned <@!{snowflake}> with reason `{reason}`.')
        else:
            await ctx.send(f"<@!{snowflake}> was already globally banned by <@!{ban['by']}> with reason `{ban['reason']}` at `{ban['date']} (UTC)`")

    @commands.Cog.listener()  # Attempt kickban on join
    async def on_member_join(self, member):
        await ban_attempt(self, member.guild, member.id)

    # @commands.Cog.listener()  # Reban if unbanned
    # async def on_member_unban(self, guild, user):
    #     await ban_attempt(self, guild, user.id)

    @commands.Cog.listener()  # Initial sweep on ready
    async def on_ready(self):
        await ban_sweep(self)

    @commands.Cog.listener()  # Sweep every 5 minutes based on member updates, which are quite frequent
    async def on_member_update(self, before, after):  # This should be called constantly, hopefully. At least once a minute
        global rate
        if time.time.diff(rate, datetime.datetime.utcnow()).seconds >= 300:  # 5 minute rate limit
            rate = datetime.datetime.utcnow()
            await ban_sweep(self)


def setup(bot):
    bot.add_cog(Moderation(bot))


async def ban_attempt(self, guild, snowflake):
    ban = await ban_list()
    if str(snowflake) in ban:
        if bDebug:
            log.debug(f'{snowflake} is flagged as globally banned')
        try:  # Try ban
            if bDebug:
                log.debug(f'Attempting ban on {snowflake}')

            # Attempt ban
            await guild.ban(tls.Snowflake(snowflake), delete_message_days=0, reason=ban[str(snowflake)]['reason'])

            if bDebug:  # reee cant make it 1 line
                log.debug(f'Ban success on {snowflake}')

            return
        except Exception:  # Missing permissions/unable
            if bDebug:
                log.debug(f'Unable to ban {snowflake}')

        try:  # Try kick
            if bDebug:
                log.debug(f'Attempting kick on {snowflake}')

            # Attempt kick
            await guild.kick(tls.Snowflake(snowflake), reason=ban[str(snowflake)]['reason'])

            if bDebug:
                log.debug(f'Kick success on {snowflake}')

            return
        except Exception:  # Missing permissions/unable
            if bDebug:
                log.debug(f'Unable to kick {snowflake}')

        if bDebug:
            log.debug(f'All attempts failed on {snowflake}')


async def ban_sweep(self):
    ban = await ban_list()
    for guild in self.bot.guilds:
        for snowflake in ban:
            if guild.get_member(snowflake):
                await ban_attempt(self, guild, snowflake)

    # for guild in self.bot.guilds:
    #     for member in guild.members:
    #         await ban_attempt(self, guild, member.id)


bl_rate = datetime.datetime.utcnow()
bl_first = True
bl_list = {}


async def ban_list():  # Use this to prevent sql errors
    host = core.json.json.orm['api']
    try:
        global bl_list
        global bl_rate
        global bl_first
        if time.time.diff(bl_rate, datetime.datetime.utcnow()).seconds >= 10 or bl_first:
            r = await core.web.Client(f"http://{host['host']}:{host['port']}/bans/list").async_get()
            bl_list = r.json()  # Can't make this a one liner cuz it tries to call await on the .json
            bl_rate = datetime.datetime.utcnow()
            bl_first = False
        return bl_list
    except Exception:
        return None
