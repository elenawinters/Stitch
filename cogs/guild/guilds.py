import discord
from discord.ext import commands
from cogs.guild.guild import *
from data.data import data
from func.funcs import *
from func.tools import *
from func import perms
import ast


class Servers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await role_assignment(member)
        await welcome_message(member, self.bot)


def setup(bot):
    bot.add_cog(Servers(bot))
