import discord
from discord.ext import commands
from core.bot.tools import *
import datetime as dt


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=[
        'stats', 'stat',
        'members',
        'servers', 'guilds',
        'ping', 'pong',
        'latency', 'lat', 'late', 'wump',
        'uptime'
    ])
    async def status(self, ctx):
        """Reveal stats about the Discord and the bot"""
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                import time
                before = time.monotonic()
                msg = await ctx.send('Grabbing status...')
                ping = round((time.monotonic() - before) * 1000)
                users = 0
                for x in self.bot.guilds:
                    users += x.member_count
                listeners = []
                for y in self.bot.cogs:  # listeners
                    cog = self.bot.get_cog(y)
                    for name, func in cog.get_listeners():
                        listeners.append(name)
                vcs = len(voice_clients(ctx))
                from core.bot.time import time
                embed = tls.Embed(ctx, title='Uptime:', description=time.uptime(time()), timestamp=True)
                embed.add_field(name=f'Members: ', value=ctx.guild.member_count)
                embed.add_field(name=f'Guilds: ', value=str(len(self.bot.guilds)))
                embed.add_field(name=f'Users: ', value=str(users))
                embed.add_field(name=f'Ping: ', value=f'{ping}ms')
                embed.add_field(name=f'Commands: ', value=str(len(self.bot.commands)))
                embed.add_field(name=f'Cogs: ', value=str(len(self.bot.cogs)))
                embed.add_field(name=f'Extensions: ', value=str(len(self.bot.extensions)))
                embed.add_field(name=f'Listeners: ', value=str(len(listeners)))
                if vcs is 1:
                    embed.add_field(name=f'Voices: ', value=f'{vcs} client')
                else:
                    embed.add_field(name=f'Voices: ', value=f'{vcs} clients')
                embed.set_footer(text=f'Latency of {round(self.bot.latency * 1000)}ms', icon_url=self.bot.user.avatar_url)
                await msg.edit(content='Here is the current status:', embed=embed)

    @commands.command()
    async def time(self, ctx):
        await ctx.send(embed=tls.Embed(ctx, timestamp=True))


def setup(bot):
    bot.add_cog(Core(bot))
