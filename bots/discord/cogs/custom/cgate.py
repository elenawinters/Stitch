""" REFERENCE guilds.pyw FOR OLD CODE """

import discord
from core.logger import log
from discord.ext import commands
from ...core.tools import tls


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def cgate(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.verification_level != discord.guild.VerificationLevel.none:
            if 'MEMBER_VERIFICATION_GATE_ENABLED' not in member.guild.features:
                await assign_role(member)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not after.pending:
            if after.guild.verification_level != discord.guild.VerificationLevel.none:
                if 'MEMBER_VERIFICATION_GATE_ENABLED' in after.guild.features:
                    await assign_role(after)

    # We can't see if the user is verified on a guild. If they start typing, we assume they are
    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        pass


def setup(bot):
    bot.add_cog(Custom(bot))


async def assign_role(member):
    log.debug(f'{member} needs to be assigned a role!')
