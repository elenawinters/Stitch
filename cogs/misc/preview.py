import discord
from discord.ext import commands
from func.tools import *
from func.funcs import *


class Preview(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embed(self, ctx, *, data=None):
        try:
            if data is None:
                embed = tls.Embed(ctx, description='Preview embeds using the [Embed Visualizer](https://leovoel.github.io/embed-visualizer/)!')
                await ctx.send(embed=embed)
            else:
                embed, message = tls.Embed.parse(ctx, data, self.bot)
                await ctx.send(content=message, embed=embed)
        except Exception as err:
            await respond(ctx, err)

    @commands.command(aliases=['emote', 'emotes', 'emoji', 'emojis', 'emoticon', 'emoticons', 'decode'])
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
