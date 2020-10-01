from discord.ext import commands
from core.logger import log
from core.bot.tools import *


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def dump(self, ctx):
        coms = []
        rem = []
        for x in self.bot.walk_commands():
            coms.append(str(x))
            for y in x.checks:
                if y.__qualname__ == 'is_owner.<locals>.predicate':
                    rem.append(str(x))

        coms = remove_duplicates(coms)
        rem = remove_duplicates(rem)
        coms = [x for x in coms if x not in rem]
        coms = remove_duplicates(coms)
        fin = []
        for x in coms:
            c = x.split(' ')
            if len(c) >= 2:
                if c[0] in coms:
                    fin.append(f'{self.bot.command_prefix}{x}')
            else:
                fin.append(f'{self.bot.command_prefix}{x}')

        p = ''
        for x in fin:
            p += f'{x}\n'

        await ctx.send(f'**Commands:**\n{p}')


def setup(bot):
    bot.add_cog(Custom(bot))
