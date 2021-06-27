import discord
from discord.ext import commands
from ..core import decorators
from ..core.tools import tls
from core.logger import log
from core import assets
from core import json
import datetime


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @decorators.permissions(2)
    async def presence(self, ctx):
        pass

    @presence.command(aliases=['activity'])
    async def game(self, ctx, _type: int, *, _game):
        try:
            # parse = _game.split(' -s ', 1)
            # if len(parse) > 1:
            #     activity = discord.Streaming(name=parse[0], url=parse[1])
            # else:
            activity = discord.Activity(type=_type, name=_game).to_dict()
            log.debug({'presence': {str(self.bot.user.id): {'activity': activity}}})
            json.orm['discord'] = {'presence': {str(self.bot.user.id): {'activity': activity}}}
            await tls.Activity.refresh(self.bot)

            embed = tls.Embed(title=assets.Game.type[activity['type']], description=activity['name'], timestamp=datetime.datetime.utcnow())

            embed.set_footer(icon_url=self.bot.user.avatar_url, text='Updated game.')
            await ctx.send(embed=embed)
        except Exception as exc:
            await tls.Message.respond(ctx, exc)

    @presence.command()
    async def status(self, ctx, stat):
        if hasattr(discord.Status, stat):
            json.orm['discord'] = {'presence': {str(self.bot.user.id): {'status': stat}}}
            await tls.Activity.refresh(self.bot)
            embed = tls.Embed(description=f'Updated status to {stat.capitalize()}', timestamp=datetime.datetime.utcnow())
        else:
            embed = tls.Embed(description='Input value is not valid', timestamp=datetime.datetime.utcnow())

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_cogs_ready(self):
        await tls.Activity.preset(self.bot)

    @commands.Cog.listener()
    async def on_resumed(self):
        await tls.Activity.preset(self.bot)


def setup(bot):
    bot.add_cog(Core(bot))
