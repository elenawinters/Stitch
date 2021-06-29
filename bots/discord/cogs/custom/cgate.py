""" REFERENCE guilds.pyw FOR OLD CODE """

import discord
from core.logger import log
from discord.ext import commands
from ...core.tools import tls
import datetime


class Custom(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def cgate(self, ctx: commands.Context):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.verification_level != discord.guild.VerificationLevel.none:
            if 'MEMBER_VERIFICATION_GATE_ENABLED' not in member.guild.features:
                await assign_role(member)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if not after.pending:
            if after.guild.verification_level != discord.guild.VerificationLevel.none:
                if 'MEMBER_VERIFICATION_GATE_ENABLED' in after.guild.features:
                    await assign_role(after)

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


async def assign_role(member: str):
    log.debug(f'{member} needs to be assigned a role!')
