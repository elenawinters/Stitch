import discord
from discord.ext import commands
from ...core import decorators
from ...core.tools import tls
from core.logger import log
from data.data import data
from core import time
from core import web
# import core.checks
import core.json
import datetime

rate = datetime.datetime.utcnow()


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['ban', 'hban'])
    @commands.check_any(decorators.permissions(3), commands.has_permissions(ban_members=True), decorators.banned())
    async def hackban(self, ctx: commands.Context, snowflake: int, *, reason: str = 'User was hackbanned'):
        try:
            await ctx.guild.ban(discord.Object(snowflake), delete_message_days=0, reason=reason)
            await ctx.send(f'Hackbanned <@!{snowflake}> with reason `{reason}`.')
        except (discord.Forbidden, discord.HTTPException) as exc:
            await tls.Message.respond(ctx, exc)
        except Exception as err:
            log.exception(err)

    @commands.command(aliases=['gban'])
    @commands.check_any(decorators.permissions(1), decorators.banned())
    async def globalban(self, ctx: commands.Context, snowflake: int, *, reason: str = 'User was globally banned'):
        ban = data.base['bans'].find_one(id=snowflake)
        if not ban:  # If None, ban
            gban = dict(
                id=snowflake,
                reason=f'{reason}',
                by=ctx.author.id,
                date=datetime.datetime.utcnow()
            )
            data.base['bans'].upsert(gban, ['id'])
            await ban_sweep(self)
            await ctx.send(f'<@!{ctx.author.id}> globally banned <@!{snowflake}> with reason `{reason}`.')
        else:
            await ctx.send(f"<@!{snowflake}> was already globally banned by <@!{ban['by']}> with reason `{ban['reason']}` at `{ban['date']} (UTC)`")

    @commands.Cog.listener()  # Attempt kickban on join
    async def on_member_join(self, member: discord.Member):
        await ban_attempt(self, member.guild, member.id)

    # @commands.Cog.listener()  # Reban if unbanned
    # async def on_member_unban(self, guild, user):
    #     await ban_attempt(self, guild, user.id)

    @commands.Cog.listener()  # Initial sweep on ready
    async def on_cogs_ready(self):
        await ban_sweep(self)

    @commands.Cog.listener()  # Sweep every 5 minutes based on member updates, which are quite frequent
    async def on_member_update(self, before: discord.Member, after: discord.Member):  # This should be called constantly, hopefully. At least once a minute
        global rate
        if time.misc.diff(rate, datetime.datetime.utcnow()).seconds >= 300:  # 5 minute rate limit
            rate = datetime.datetime.utcnow()
            await ban_sweep(self)


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))


async def ban_attempt(self: tls.Cog.pseudo, guild: discord.Guild, snowflake: int):  # this code needs to be re-tested
    ban = await ban_list()
    if str(snowflake) in ban:
        # if tls.attempt()
        # log.debug('ban attempting')
        # if await tls.attempt(guild.ban, discord.Object(snowflake), delete_message_days=0, reason=ban[str(snowflake)]['reason']) is tls.Types.NoReturn:
        #     await tls.attempt(guild.kick, discord.Object(snowflake), reason=ban[str(snowflake)]['reason'])
        try:
            await guild.ban(discord.Object(snowflake), delete_message_days=0, reason=ban[str(snowflake)]['reason'])
            return
        except Exception:
            pass
        try:
            await guild.kick(discord.Object(snowflake), reason=ban[str(snowflake)]['reason'])
            return
        except Exception:
            pass


async def ban_sweep(self: tls.Cog.pseudo):
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
    try:
        global bl_list
        global bl_rate
        global bl_first
        if time.misc.diff(bl_rate, datetime.datetime.utcnow()).seconds >= 1800 or bl_first:
            bl_list = (await web.api('bans').async_get()).json()
            bl_rate = datetime.datetime.utcnow()
            bl_first = False
        return bl_list
    except Exception as exc:
        log.exception(exc)
        return []
