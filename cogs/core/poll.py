import discord
from discord.ext import commands
from core.bot import settings
from core.bot.tools import *
from core.bot import perms
import core.checks
color = discord.Colour.from_rgb(r=59, g=136, b=195)


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='vote')
    @settings.enabled()
    @perms.has_perms()
    @core.checks.is_banned()
    async def vote(self, ctx, *, msg=''):
        """Command to open vote
        `.vote [text]`"""
        try:
            if len(msg) > 0:
                embed = tls.Embed(ctx, title=f"Vote by **{ctx.author}**:", description=msg)
                vote = await ctx.send(embed=embed)
                await vote.add_reaction(u"\U0001F53C")  # UP ARROW
                await vote.add_reaction(u"\U0001F53D")  # DOWN ARROW
            else:
                await ctx.send('You need to vote on something!')
        except Exception as e:
            await ctx.send(f'Something went wrong. {e}')

    @commands.command(name='poll')
    @settings.enabled()
    @perms.has_perms()
    @core.checks.is_banned()
    async def poll(self, ctx, amount, *, msg=''):
        """Command to open poll
        `.poll [number of options] [text]`"""
        base = ord(u"\U0001F1E6")  # INDICATOR A
        try:
            if is_number(amount):
                if 2 <= int(amount) <= 20:
                    if len(msg) > 0:
                        embed = tls.Embed(ctx, title=f"Poll by **{ctx.author}**:", description=msg)
                        poll = await ctx.send(embed=embed)
                        for x in range(0, int(amount)):
                            options = base + x
                            indicator = chr(options)
                            await poll.add_reaction(indicator)  # REGIONAL INDICATORS
                    else:
                        await ctx.send('You need to poll on something!')
                else:
                    await ctx.send('Number of options out of range')
            else:
                await ctx.send('You need to enter a number!')
        except Exception as e:
            await ctx.send(f'Something went wrong. {e}')

    @commands.command(name='ask', aliases=['question', 'questions'])
    @settings.enabled()
    @perms.has_perms()
    @core.checks.is_banned()
    async def ask(self, ctx, *, msg):
        """Command to ask question
        `.ask [text]`"""
        try:
            if len(msg) > 0:
                embed = tls.Embed(ctx, title=f"Question by **{ctx.author}**:", description=msg)
                ask = await ctx.send(embed=embed)
                await ask.add_reaction(u"\U0001F1FE")  # Y SYMBOL
                await ask.add_reaction(u"\U0001F1F3")  # N SYMBOL
            else:
                await ctx.send('You need to ask something!')
        except Exception as e:
            await ctx.send(f'Something went wrong. {e}')


def setup(bot):
    bot.add_cog(Core(bot))
