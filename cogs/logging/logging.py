import discord
from discord.ext import commands
from core.color import trace
from core.logger import log


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_server_join(self, server):
        log.info(f'> Joined {server.name}')

    @commands.Cog.listener()
    async def on_server_remove(self, server):
        log.error(f'> Removed from {server.name}')


def setup(bot):
    bot.add_cog(Logs(bot))
