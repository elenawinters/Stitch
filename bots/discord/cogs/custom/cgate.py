""" REFERENCE guilds.pyw FOR OLD CODE """
# TODO: FINISH THIS FFS

import discord
from core.logger import log
from discord.ext import commands
from ...core.tools import tls
from data.data import data
import datetime


class Custom(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def cgate(self, ctx: commands.Context):
        pass

    async def member_joined(self, member: discord.Member, guid=None):
        status = data.base['cgate'].find_one(type='join', serverid=member.guild.id if guid is None else guid)
        if status is None:
            return 'No data found'
        log.debug(f'{member} needs to be welcomed!')

    async def member_left(self, member: discord.Member):
        log.debug(f'{member} needs to be shamed!')

    async def assign_role(self, member: discord.Member, guid=None):
        roles = data.base['cgate'].find_one(serverid=member.guild.id)
        log.debug(f'{member} needs to be assigned a role!')

    async def revoke_role(self, member: discord.Member):
        log.debug(f"{member}'s role needs to be revoked!")
        log.debug('This function is not yet implemented.')
        raise NotImplementedError

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.member_joined(member)
        if member.guild.verification_level != discord.guild.VerificationLevel.none:
            if 'MEMBER_VERIFICATION_GATE_ENABLED' not in member.guild.features:
                await self.assign_role(member)

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member):
        await self.member_left(member)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if not after.pending and after.guild.verification_level != discord.guild.VerificationLevel.none:
            if 'MEMBER_VERIFICATION_GATE_ENABLED' in after.guild.features:
                await self.assign_role(after)

    # We can't see if the user is verified on a guild. If they start typing, we assume they are
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_typing(self, channel: discord.TextChannel, user: discord.User, when: datetime.datetime):
        if member := channel.guild.get_member(user.id):
            # if 'MEMBER_VERIFICATION_GATE_ENABLED' in after.guild.features:
            # if after.guild.verification_level != discord.guild.VerificationLevel.none:
            #     if 'MEMBER_VERIFICATION_GATE_ENABLED' in after.guild.features:
            pass
        pass


def setup(bot: commands.Bot):
    bot.add_cog(Custom(bot))
