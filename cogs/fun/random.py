import discord
from discord.ext import commands
from core.ext.enums import general
from core.ext.enums import names
from core.bot.tools import tls
import httpx as requests
import core.checks
import random


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name='name', aliases=['handmeaname', 'hman', 'names'])
    @core.checks.is_banned()
    async def name_generator(self, ctx, sex=None, *, seed=None):
        """Name generator.
        `.name [sex] [seed]`
        Sexes:
        : Male - 1, M
        : Female - 2, F
        : Other - 3, Default"""
        if sex is None:
            if seed is not None:
                random.seed(seed)
            sex = random.randint(1, 3)
        sex = tls.Enums(general.Sex).find(sex)
        if sex.value == 1:  # First Names
            fr = names.NameURLs.male
        elif sex.value == 2:
            fr = names.NameURLs.female
        else:
            fr = names.NameURLs.first
        mr = names.NameURLs.middle
        lr = names.NameURLs.last
        f = requests.get(fr.value).json()['data']  # First
        m = requests.get(mr.value).json()['RandL']['items']  # Middle
        la = requests.get(lr.value).json()['data']  # Last
        lt = la
        if seed is not None:
            random.seed(seed)
        f = random.choice(f)
        if seed is not None:  # So middle name is not always the same between sexes
            if sex.value == 2:  # Female gets default, others get extra seeding.
                random.seed(seed)
            else:
                random.seed(f'{sex.value}{seed}')
                # random.seed(f'{seed}{seed}')
        m = random.choice(m)
        if seed is not None:
            random.seed(seed)
        la = random.choice(la)
        if seed is not None:
            random.seed(seed)
        lx = random.randint(1, 6)
        if lx == 2 or lx == 6:
            if seed is not None:
                random.seed(f'{seed}-{seed}')
            lx = random.choice(lt)
            if seed is not None:
                random.seed(seed)
            r = random.randint(1, 2)
            if r == 1:
                la = f'{la}-{lx}'
            else:
                la = f'{lx}-{la}'
        embed = tls.Embed(description=f'{f} {m} {la}', timestamp=True)
        if seed is None:
            seed = 'Random'
        embed.set_footer(text=f'{sex.value} | {seed}')
        await ctx.send(embed=embed)
        # embed = tls.Embed
        # await ctx.send(f'> {f} {l}')
        # print(f'> {f} {l}')

        # print('HAND ME A NAME')


def setup(bot):
    bot.add_cog(Fun(bot))
