import discord
from discord.ext import commands
import sys, traceback

from func.color import trace
from func.funcs import log, error, warn
from func.funcs import extensions
from func.json import json as jsons
from func.enums import ReturnType
from func.json import protected
from func.tools import *


class JSON(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='json', hidden=True)
    @commands.is_owner()
    async def json(self, ctx):
        args = ctx.message.content.split(' ')
        if len(args) >= 2:
            if args[1] not in protected:
                value = jsons.reader(args[1])
                if len(args) == 2:  # READ
                    await ctx.send(f'Reading \'{args[1]}\' as "{value}"')
                elif len(args) >= 3:  # APPEND
                    if value != ReturnType.fail:
                        remainder = split_string(ctx.message.content, f'{args[0]} {args[1]} ')
                        jsons.update(args[1], remainder)
                        await ctx.send(f'Appended \'{args[1]}\' with "{jsons.reader(args[1])}"')
                else:
                    await ctx.send(f'Not enough arguments')
            else:
                await ctx.send(f'That value is protected')
        else:
            await ctx.send(f'Not enough arguments')


def setup(bot):
    bot.add_cog(JSON(bot))
