from discord.ext import commands


class Zaqistan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    if bot.user.id == 849541560928567297:
        bot.add_cog(Zaqistan(bot))
