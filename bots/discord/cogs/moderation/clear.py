import discord
from discord.ext import commands
from ...core import decorators


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['purge', 'claer'])
    @decorators.banned()  # TODO: this is completely broken. gonna have to revisit this
    async def clear(self, ctx: commands.Context, limit: float = 1):  # arg used to be a str
        """Clears up to 250 messages
        .clear [number of messages]"""
        try:
            await ctx.message.delete()
        except Exception:
            pass

        if int(limit) <= 250:  # Hard limit.
            await ctx.message.channel.purge(limit=int(limit))
        else:
            await ctx.send(f'Cannot clear more than 250 messages')


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
