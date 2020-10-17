import discord
from discord.ext import commands
from ...core import decorators
from ...core.tools import tls


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='say', aliases=['me'], hidden=True)
    @decorators.permissions(3)
    @decorators.banned()
    async def say(self, ctx, *, arg=''):
        """Make the bot say something!
        `.say [text]`"""
        if len(arg) > 0:
            embed = tls.Embed(ctx, description=arg, colour=get_color(ctx))
            await ctx.send(embed=embed)

    @commands.command(name='sudo', aliases=['echo'], hidden=True)
    @decorators.permissions(3)
    @decorators.banned()
    async def sudo(self, ctx, *, arg=''):
        """Make the bot say something!
        `.sudo [text]`"""
        if len(arg) > 0:
            await ctx.send(arg)


def setup(bot):
    bot.add_cog(Core(bot))
