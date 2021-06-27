from discord.ext import commands
from ...core.tools import tls


class Zaqistan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    if tls.cog.botSpecific(849541560928567297, bot):
        bot.add_cog(Zaqistan(bot))
