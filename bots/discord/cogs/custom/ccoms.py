import discord
from discord.ext import commands
from data.data import data
from ...core.tools import tls
from ...core import decorators
import ast


def match(obj, find):  # Returns key, you can match the key with the dict to get the value
    for k, v in d1.items():  # lol what where is d1. no idea what this does anymore
        if isinstance(k, str):
            if find == k:
                return k
        else:
            for x in k:
                if find == x:
                    return k
    return None


class Ext(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(aliases=['ccom'])
    @decorators.permissions('admin')
    @decorators.banned()
    async def ccoms(self, ctx):
        pass

    @ccoms.command()
    @decorators.permissions('admin')
    async def remove(self, ctx: commands.Context, name: str):
        ccom = dict(ast.literal_eval(data.base['ccom'].find_one(server=ctx.guild.id)['commands']))
        ccom.pop(name, None)
        ccom = dict(
            server=ctx.guild.id,
            commands=str(ccom)
        )
        data.base['ccom'].upsert(ccom, ['server'])
        await ctx.send(f'Removed cCom `{name}`')

    @ccoms.command(aliases=['edit', 'overwrite', 'update', 'create'])
    @decorators.permissions('admin')
    async def add(self, ctx: commands.Context, name: str, *, content: str):
        try:
            ccom = dict(ast.literal_eval(data.base['ccom'].find_one(server=ctx.guild.id)['commands']))
        except TypeError:
            ccom = {}
        com = {name: content}
        ccom.update(com)
        ccom = dict(
            server=ctx.guild.id,
            commands=str(ccom)
        )
        data.base['ccom'].upsert(ccom, ['server'])
        await ctx.send(f'Updated cCom `{name}`')

    @ccoms.group()
    @decorators.permissions('admin')
    async def alias(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        com_name = list(msg.content)
        if len(com_name) > 0:
            if com_name[0] == self.bot.command_prefix:
                try:
                    ccom = dict(ast.literal_eval(data.base['ccom'].find_one(server=msg.guild.id)['commands']))
                except TypeError:
                    ccom = {}
                cname = tls.split(msg.content, f'{self.bot.command_prefix}').split(' ')[0]
                if cname in ccom:
                    # print(ccom[cname])
                    await msg.channel.send(ccom[cname])


def setup(bot: commands.Bot):
    bot.add_cog(Ext(bot))
