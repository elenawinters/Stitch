import discord
from discord.ext import commands
from data.data import data
from core.bot.funcs import *
from core.bot.tools import *
import json
import ast

# async def

async def welcome_message(member, bot=None, guid=None):
    if guid is not None:
        status = data.base['welcome_message'].find_one(serverid=guid)
    else:
        status = data.base['welcome_message'].find_one(serverid=member.guild.id)
    if status is not None:
        embed, message = tls.Embed.parse(member, status['embed'], bot)
        if status['channelid'] is not None:
            channel = member.guild.get_channel(int(status['channelid']))
        else:
            channel = member.guild.system_channel
        if channel is not None:
            await channel.send(message, embed=embed)


async def role_assignment(member):
    roles = data.base['role_assignment'].find_one(serverid=member.guild.id)
    if roles is not None:
        roles = roles['roles'].split()
        for x in roles:
            try:
                role = member.guild.get_role(int(x))
                if role is not None:
                    if role in member.guild.roles:
                        try:
                            await member.add_roles(role, reason='Default role for Discord server.')
                        except Exception:
                            pass
            except Exception:
                pass


