import discord
from discord.ext import commands
from func.time import time
import datetime


class Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

        # print(json.reader('test', 'test.txt'))

        # n1 = ctx.author.created_at
        # n2 = datetime.datetime.utcnow()
        # r = time.diff(n1, n2)
        # # r = datetime.timedelta(days=5)
        # age = time.readable.From.timedelta.seconds(r)
        # h = 15 * int(r.days)
        # print(h)
        # if h > 120:
        #     h = 120
        # color = tls.Color.from_hsv(h)
        # print(color.to_rgb())
        # print(color.value)
        # embed = tls.Embed(ctx, description=f'Information about {ctx.author.mention} **({ctx.author})**', timestamp=ctx.author.created_at, colour=color)
        # embed.add_field(name='Identifier:', value=f'`{ctx.author.id}`', inline=True)
        # embed.add_field(name='Created At:', value=f'`{ctx.author.created_at}`', inline=True)
        # embed.add_field(name=f'Account Age:', value=f'```{age}```', inline=False)
        # embed.set_thumbnail(url=ctx.author.avatar_url)
        # if r.days < 3:
        #     embed.set_footer(icon_url=assets.Discord.progress[h], text='Very Suspicious')
        # elif r.days < 5:
        #     embed.set_footer(icon_url=assets.Discord.progress[h], text='Suspicious')
        # elif r.days < 7:
        #     embed.set_footer(icon_url=assets.Discord.progress[h], text='Slightly Suspicious')
        # else:
        #     embed.set_footer(icon_url=assets.Discord.progress[h], text='Not Suspicious')
        # await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Ext(bot))
