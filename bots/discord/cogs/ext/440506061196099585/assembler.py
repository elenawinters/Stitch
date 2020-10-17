from discord.ext import commands
from ....core import decorators
from ....core.tools import tls
from core.logger import log
import discord


class Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @decorators.banned()
    async def assemble(self, ctx):
        assembler = []
        async with ctx.typing():
            async for x in ctx.message.channel.history(limit=500):
                if len(x.content.split(' ')) < 4:
                    if x.content and not x.content.startswith(f'{self.bot.command_prefix}{ctx.command.name}'):
                        assembler.insert(0, x.content)
                else: break

            if assembled := ' '.join(assembler):
                await ctx.send(assembled)
            else:
                await ctx.send(f"There's nothing to {ctx.command.name}!")


def setup(bot):
    bot.add_cog(Ext(bot))
