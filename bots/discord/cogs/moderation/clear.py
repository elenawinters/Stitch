import discord
from discord.ext import commands
from ...core import decorators


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['purge', 'claer'])
    @decorators.banned()
    async def clear(self, ctx: commands.Context, arg: int = 1):  # arg used to be a str
        """Clears up to 250 messages
        .clear [number of messages]"""
        try:
            await ctx.message.delete()
        except Exception:
            pass
        if len(arg) > 0:
            if isinstance(arg, float):
                if int(arg) <= 250:  # Hard limit.
                    await ctx.message.channel.purge(limit=int(arg))
                else:
                    await ctx.send(f'Cannot clear more than 250 messages')
            else:
                await ctx.send(f'You need to specify a number!')
        else:
            await ctx.send(f'You need to specify how much you want to clear')

    # # To globally ban an account.
    # @commands.command()
    # @commands.is_owner()
    # async def globalban(self, ctx, snowflake):
    #     pass


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
