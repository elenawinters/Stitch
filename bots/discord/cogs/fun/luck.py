import discord
from discord.ext import commands
from core import assets
from core.bot.tools import tls
import core.checks
import random


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', aliases=['rolls', 'dice', 'rolldice', 'diceroll', 'rol'])
    @core.checks.is_banned()
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
    @core.checks.is_banned()
    async def flip_coin(self, ctx):
        flip = random.randint(1, 2)
        embed = tls.Embed(ctx, description=f'You flipped a coin!', timestamp=True)
        if flip == 1:
            embed.set_thumbnail(url='https://www.mediafire.com/convkey/e737/0w5u9efs03xo5gxzg.jpg')
            embed.set_footer(text='It landed on Heads!')
        else:
            embed.set_thumbnail(url='https://www.mediafire.com/convkey/43a4/tcrxt39knsguqm6zg.jpg')
            embed.set_footer(text='It landed on Tails!')
        await ctx.send(embed=embed)

    @commands.command(name='number', aliases=['random', 'rand', 'num', 'randomnumber', 'rando'])
    @core.checks.is_banned()
    async def number_generator(self, ctx, number='1-100', *, seed=None):
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


def setup(bot):
    bot.add_cog(Fun(bot))
