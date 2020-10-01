from discord.ext import commands
from core.logger import log
from core.bot.tools import *


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def emote_test(self, ctx):
        await ctx.send('<:berryTracer:623441438830624782>')


def setup(bot):
    bot.add_cog(Custom(bot))
