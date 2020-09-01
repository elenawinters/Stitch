import discord
from discord.ext import commands
from core.bot.tools import tls
from cogs.custom import cmus
from core.logger import log
import datetime
import asyncio
import os
do_fool = False


class Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def fool(self, ctx):
        global do_fool
        do_fool = not do_fool

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        date = datetime.date.today()
        # if True:
        if do_fool or (date.month == 4 and date.day == 1):
            bot = cmus.Player.self(self, member)
            if bot.voice is not None:
                if member.id is not self.bot.user.id:
                    if before.channel is not after.channel:
                        if after.channel is bot.guild.voice_client.channel:
                            path = 'cogs\\ext\\aprilfools\\somebody.mp3'
                            await cmus.Player.play.file(path, bot)

    @commands.command()
    @commands.is_owner()
    async def somebody(self, ctx):
        path = 'cogs\\ext\\aprilfools\\somebody.mp3'
        if cmus.Player.is_connected(ctx):
            await cmus.Player.play.file(path, ctx.me)
        else:
            if await cmus.Player.can_connect(ctx, False):
                await cmus.Player.join(ctx.message.author)
                duration = await cmus.Player.play.file(path, ctx.me)
                await asyncio.sleep(duration + 0.2)
                await cmus.Player.disconnect(ctx.me)


def setup(bot):
    bot.add_cog(Ext(bot))
