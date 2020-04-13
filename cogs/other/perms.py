import discord
from discord.ext import commands

from func.color import trace
from func.funcs import log, error
from func.funcs import extensions
from func import perms as perm

class Perms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='perms', aliases=['perm', 'permission', 'permissions'], hidden=True)
    async def perms(self, ctx):
        """Command to perm test response"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f'perm test')

    @perms.command(name='add')
    @perm.is_admin()
    async def add(self, ctx):
        args = ctx.message.content.split(' ')

        if len(ctx.message.mentions) > 0:
            for x in ctx.message.mentions:
                args.remove(str(x.mention))

            for x in ctx.message.mentions:
                try:
                    print(perm)
                    perm.perms.add()
                except Exception as e:
                    print(e)
                # This will add/remove the perms once I write
                # up the system for it
        else:
            await ctx.send(f'No user mentioned.')
        #print(len(ctx.message.mentions))
            #print(x)
        #print(ctx.message.channel.permissions_for(ctx.message.author).administrator)
        await ctx.send(f'perm add test')

    @perms.command(name='remove')
    @perm.is_admin()
    async def remove(self, ctx):
        args = ctx.message.content.split(' ')

        if len(ctx.message.mentions) > 0:
            for x in ctx.message.mentions:
                args.remove(str(x.mention))

            for x in ctx.message.mentions:
                try:
                    print(perm)
                    perm.perms.remove()
                except Exception as e:
                    print(e)
                # This will add/remove the perms once I write
                # up the system for it
        else:
            await ctx.send(f'No user mentioned.')
        #print(len(ctx.message.mentions))
            #print(x)
        #print(ctx.message.channel.permissions_for(ctx.message.author).administrator)
        await ctx.send(f'perm remove test')

    @perms.command(name='update')
    @perm.is_admin()
    async def update(self, ctx):
        args = ctx.message.content.split(' ')

        if len(ctx.message.mentions) > 0:
            for x in ctx.message.mentions:
                args.remove(str(x.mention))

            for x in ctx.message.mentions:
                try:
                    print(perm)
                    perm.perms.update()
                except Exception as e:
                    print(e)
                # This will add/remove the perms once I write
                # up the system for it
        else:
            await ctx.send(f'No user mentioned.')
        #print(len(ctx.message.mentions))
            #print(x)
        #print(ctx.message.channel.permissions_for(ctx.message.author).administrator)
        await ctx.send(f'perm update test')

def setup(bot):
    bot.add_cog(Perms(bot))


