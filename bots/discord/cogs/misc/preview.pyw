import discord
from discord.ext import commands
from core.bot.tools import *
from core.bot.funcs import *
import core.checks


class Preview(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @core.checks.is_banned()
    async def embed(self, ctx, *, data=None):
        try:
            if data is None:
                embed = tls.Embed(ctx, description='Preview embeds using one of two [Embed Visualizers](https://leovoel.github.io/embed-visualizer/)!')
                await ctx.send(embed=embed)
            else:
                embed, message = tls.Embed.parse(ctx, data, self.bot)
                await ctx.send(content=message, embed=embed)
        except Exception as err:
            await respond(ctx, err)

    @commands.command(aliases=['emote', 'emotes', 'emoji', 'emojis', 'emoticon', 'emoticons', 'decode'])
    @core.checks.is_banned()
    async def code(self, ctx, *, emote=None):
        try:
            if emote is not None:
                embed = tls.Embed(ctx, description=f'Discord code for {emote}:\n`{emote}`')
                await ctx.send(embed=embed)
            else:
                embed = tls.Embed(ctx, description='You need to specify something to decode!')
                await ctx.send(embed=embed)
        except Exception as err:
            await respond(ctx, err)

    @commands.command(aliases=['colour'])
    @core.checks.is_banned()
    async def color(self, ctx, *, emote=None):
        try:
            if emote is not None:
                embed = tls.Embed(ctx, description=f'Discord code for {emote}:\n`{emote}`')
                await ctx.send(embed=embed)
            else:
                embed = tls.Embed(ctx, description='You need to specify something to decode!')
                await ctx.send(embed=embed)
        except Exception as err:
            await respond(ctx, err)


def setup(bot):
    bot.add_cog(Preview(bot))
