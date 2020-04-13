import discord
from discord.ext import commands
from func.ext import assets
from func.tools import tls
from func.funcs import dbg
import random


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', aliases=['rolls', 'dice', 'rolldice', 'diceroll', 'rol'])
    async def roll_dice(self, ctx, dice='1d6', extra=None):
        """Roll a dice!
        `.roll [type]`
        Type:
        [number of dice to roll] d [number of sides the dice has]
        """
        if dice != '1d2':
            d = dice.split('d')
            rolls = []
            total = 0
            # Hard limits
            if int(d[0]) >= 1000000:
                d[0] = '1000000'
            if int(d[1]) >= 1000000000000:
                d[1] = '1000000000000'
            dice = f'{d[0]}d{d[1]}'
            for x in range(int(d[0])):
                roll = random.randint(1, int(d[1]))
                rolls.append(roll)
                total += roll
                # print(roll)
                # dbg(roll)
            r_rolls = rolls
            rolls = str(rolls)[1:-1]
            embed = tls.Embed(ctx, description=f'You rolled a {total}!')
            text = f'{dice} die | Rolled {rolls}'[:2039]
            if len(text) >= 2039 and len(r_rolls) > 1:
                text = f'{text}, more...'
            # dbg(r_rolls)
            embed.set_footer(text=text)
            await ctx.send(embed=embed)
        else:
            await tls.Command.execute(self, ctx, 'coin')

    @commands.command(name='coin', aliases=['flip', 'flipcoin', 'coinflip'])
    async def flip_coin(self, ctx):
        flip = random.randint(1, 2)
        embed = tls.Embed(ctx, description=f'You flipped a coin!', timestamp=True)
        if flip == 1:
            embed.set_thumbnail(url=assets.Images.Coins.Quarter.heads)
            embed.set_footer(text='It landed on Heads!')
        else:
            embed.set_thumbnail(url=assets.Images.Coins.Quarter.tails)
            embed.set_footer(text='It landed on Tails!')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))


