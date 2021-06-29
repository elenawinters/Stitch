import discord
from discord.ext import commands
from ...core import decorators
from ...core.tools import tls
from core.logger import log
from core import assets
import random


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='roll', aliases=['rolls', 'dice', 'rolldice', 'diceroll', 'rol'])
    @decorators.banned()
    async def roll_dice(self, ctx: commands.Context, dice: str = '1d6', extra=None):
        """Roll a dice!
        `.roll [type]`
        Type:
        [number of dice to roll] d [number of sides the dice has]
        """
        if dice == '1d2':
            await tls.Command.execute(self, ctx, 'coin')
            return
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

    @commands.command(name='coin', aliases=['flip', 'flipcoin', 'coinflip'])
    @decorators.banned()
    async def flip_coin(self, ctx: commands.Context):
        flip = random.choice(['heads', 'tails'])
        embed = tls.Embed(ctx, description=f'You flipped a coin!', timestamp=True)

        embed.set_thumbnail(url=getattr(assets.Misc.coin, flip))
        embed.set_footer(text=f"It landed on {flip.capitalize()}!")
        await ctx.send(embed=embed)

    @commands.command(name='number', aliases=['random', 'rand', 'num', 'randomnumber', 'rando'])
    @decorators.banned()
    async def number_generator(self, ctx: commands.Context, number: str = '1-100', *, seed=None):
        """Pseudorandom number generator.
        `.number [range] [seed]`
        Examples:
        : .number 1-100
        : .number 1-100 Test
        """
        channel = [
            'r', 'radio',
            'radiochannel',
            'setradiochannel'
        ]
        phone = [
            'n', 'number',
            'phonenumber',
            'phone'
        ]
        if number in channel:
            number = '0-256'
        if number in phone:
            number = '1000000-9999999'
        n = number.split('-')
        if seed is not None:
            random.seed(seed)
        number = random.randint(int(n[0]), int(n[1]))
        embed = tls.Embed(description=f'Pseudorandom number in range from {n[0]} to {n[1]}', timestamp=True)
        # embed = tls.Embed(timestamp=False)
        if seed is None:
            seed = 'Random'
        embed.set_footer(text=f'{number} | {seed}')
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
