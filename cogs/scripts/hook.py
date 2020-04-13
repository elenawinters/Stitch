import discord
from func.funcs import *
from discord.ext import commands
from cogs.scripts import loader
from data.data import data
from func import settings
from func.enums import *
from func.tools import *
import random


class Puzzles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # @commands.dm_only()
    # async def name(self, ctx, *, name=None):
    #     try:
    #         if name is None:
    #             name = data.base['profile'].find_one(user_id=ctx.author.id)['name']
    #         else:
    #             data.base['profile'].upsert(dict(user_id=ctx.author.id, name=name), ['user_id'])
    #         await ctx.send(f'Your name: {name}')
    #     except Exception:
    #         pass

    @commands.Cog.listener()
    async def on_message(self, msg):
        if type(msg.channel) == discord.DMChannel:
            if not msg.content.startswith(self.bot.command_prefix):
                try:
                    await loader.loader(self, msg)
                except Exception as err:
                    error(err)
        pass
        # log(f'> Joined {server.name}', enums.LogLevel.default)

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     try:
    #         await member.create_dm()
    #     except Exception:
    #         pass
    #     await member.dm_channel.send('Hello! Welcome to the Firebug Puzzle.\n'
    #                                  'First things first, this is meant to be an **in character** conversation between your character and a website.\n'
    #                                  'Do not abuse the bot. It is still in early development and may encounter issues.\n'
    #                                  'All conversations between you and this Discord bot are logged.\n'
    #                                  'Thank you for reading and enjoy the Firebug Puzzle!\n\n'
    #                                  'Start by saying something to the bot!')

    # @commands.command()
    # @commands.dm_only()
    # async def perma(self, ctx):
    #     try:
    #        data.base['progress'].upsert(dict(user_id=ctx.author.id, chapter=0, page=0), ['user_id'])
    #        await ctx.send('Reset progress successfully.')
    #     except Exception as err:
    #        await respond(ctx, err)

    @commands.command()
    async def tell(self, ctx, user, *, message):
        try:
            try:
                user = await commands.MemberConverter().convert(ctx=ctx, argument=user)
            except commands.BadArgument:
                try:
                    user = await commands.UserConverter().convert(ctx=ctx, argument=user)
                except commands.BadArgument:
                    try:
                        user = tls.search(user, self.bot.users)[0]
                    except IndexError:
                        user = None
            if user is not None:
                try:
                    await user.create_dm()
                except Exception:
                    pass
                await user.dm_channel.send(message)
        except Exception as err:
            await respond(ctx, err)


def setup(bot):
    bot.add_cog(Puzzles(bot))
