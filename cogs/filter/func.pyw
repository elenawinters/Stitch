import discord
from discord.ext import commands
from data.data import data

from func.color import trace
from func.funcs import *
from data.data import data


class Filters:
    @classmethod
    def get(cls, ctx):
        for x in dbFilter(ctx, 'filter'):
            print(x)

    @classmethod
    def set(cls, ctx):
        pass


class Exceptions:
    @classmethod
    def get(cls, ctx):
        for x in dbFilter(ctx, 'exceptions'):
            print(x)

    @classmethod
    def set(cls, ctx):
        pass


def dbFilter(ctx, rtype):
    dbdata = data.base['filter'].find_one(serverid=ctx.guild.id, enabled=True)
    if dbdata is not None:
        if dbdata['enabled'] is True:
            if dbdata['use_default'] is True:
                dbdata = data.base['filter'].find_one(serverid=0)
        try:
            return dbdata[rtype]
        except KeyError:
            return []

    return []


exceptions = Exceptions
filters = Filters






