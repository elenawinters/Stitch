import discord
from discord.ext import commands
from core.ext import assets
from core.bot.tools import tls
from core import json
import datetime


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def game(self, _type, *, _game):
        pass

    @commands.command(aliases=['stream'])
    @commands.is_owner()
    async def game(self, ctx, _type: int, *, _game):
        parse = _game.split(' -s ', 1)
        if len(parse) > 1:
            activity = discord.Streaming(name=parse[0], url=parse[1])
        else:
            activity = discord.Activity(type=_type, name=_game, flags=None)
            jack = json.json.orm['activity']
            jack[str(self.bot.user.id)] = activity.to_dict()
            json.json.orm['activity'] = jack
            # json.json.orm['activity'][self.bot.user.id] = activity.to_dict()
        await self.bot.change_presence(activity=activity)
        activity = activity.to_dict()
        if activity['type'] == 1:
            embed = tls.Embed(title=assets.Game.type[activity['type']], description=activity['name'], url=activity['url'], timestamp=datetime.datetime.utcnow())
        else:
            embed = tls.Embed(title=assets.Game.type[activity['type']], description=activity['name'], timestamp=datetime.datetime.utcnow())
        embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'Updated game.')
        await ctx.send(embed=embed)

    @commands.command(aliases=['unstream'])
    @commands.is_owner()  # Name will probably change
    async def reset(self, ctx):
        await tls.Activity.preset(self.bot)

    @commands.Cog.listener()
    async def on_ready(self):
        await tls.Activity.preset(self.bot)

    @commands.Cog.listener()
    async def on_resumed(self):
        await tls.Activity.preset(self.bot)


def setup(bot):
    bot.add_cog(Core(bot))
