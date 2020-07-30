import discord
from discord.ext import commands
from data.data import data
from core.bot.funcs import *
from core.bot.tools import *
from core.bot import perms
import core.checks
import ast


class Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['ccom'])
    @perms.is_admin()
    @core.checks.is_banned()
    async def ccoms(self, ctx):
        pass

    @ccoms.command()
    @perms.is_admin()
    async def remove(self, ctx, name: str):
        ccom = ast.literal_eval(data.base['ccom'].find_one(server=ctx.guild.id)['commands'])
        ccom.pop(name, None)
        ccom = dict(
            server=ctx.guild.id,
            commands=str(ccom)
        )
        data.base['ccom'].upsert(ccom, ['server'])
        await ctx.send(f'Removed cCom `{name}`')

    @ccoms.command(aliases=['edit', 'overwrite', 'update', 'create'])
    @perms.is_admin()
    async def add(self, ctx, name: str, *, content: str):
        try:
            ccom = ast.literal_eval(data.base['ccom'].find_one(server=ctx.guild.id)['commands'])
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

    @commands.Cog.listener()
    async def on_message(self, msg):
        com_name = list(msg.content)
        if len(com_name) > 0:
            if com_name[0] == self.bot.command_prefix:
                try:
                    ccom = ast.literal_eval(data.base['ccom'].find_one(server=msg.guild.id)['commands'])
                except TypeError:
                    ccom = {}
                cname = split_string(msg.content, f'{self.bot.command_prefix}').split(' ')[0]
                if cname in ccom:
                    # print(ccom[cname])
                    await msg.channel.send(ccom[cname])


def setup(bot):
    bot.add_cog(Ext(bot))
