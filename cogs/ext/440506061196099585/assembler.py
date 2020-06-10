from discord.ext import commands


class Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def assemble(self, ctx):
        test = ''
        async with ctx.typing():
            for x in reversed(await ctx.message.channel.history(limit=500).flatten()):
                if len(x.content.split(' ')) < 4:
                    start = True
                else:
                    start = False
                    test = ''

                if start is True:
                    if x.content != f'{self.bot.command_prefix}assemble':
                        test += f'{x.content} '
            await ctx.send(test)


def setup(bot):
    bot.add_cog(Ext(bot))

