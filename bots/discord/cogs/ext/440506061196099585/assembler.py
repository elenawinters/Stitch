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
    async def assemble(self, ctx, limit=4):
        assembler = []
        async with ctx.typing():
            async for x in ctx.message.channel.history(limit=500):
                if len(x.content.split(' ')) < limit:
                    if x.content and not x.content.startswith(f'{self.bot.command_prefix}{ctx.command.name}'):
                        assembler.insert(0, x.content)
                else: break

            if assembled := ' '.join(assembler):
                try: await ctx.send(assembled)
                except Exception as exc:
                    await tls.Message.respond(ctx, exc)
            else:
                await ctx.send(f"There's nothing to {ctx.command.name}!")


def setup(bot):
    bot.add_cog(Ext(bot))
