import discord
from discord.ext import commands
from ...core.tools import tls
from core.logger import log
from core import json
from core import time
from core import web
import asyncio
import httpx


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=[
        'stats', 'stat',
        'members',
        'servers', 'guilds',
        'ping', 'pong',
        'latency', 'lat', 'late', 'wump',
        'uptime', 'time'
    ])
    async def status(self, ctx):
        """Reveal stats about the Discord and the bot"""
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                try:
                    # Ping
                    msg_embed = tls.Embed(description='Grabbing status...')
                    before = time._time.monotonic()
                    msg = await ctx.send(embed=msg_embed)
                    ping = round((time._time.monotonic() - before) * 1000)

                    host = json.orm['api']
                    api_before = time._time.monotonic()
                    r = await web.Client(f"http://{host['host']}:{host['port']}/stat/").async_get()
                    api_ping = round((time._time.monotonic() - api_before) * 1000)
                    # log.debug(r.content)

                    guilds = 'N/A'
                    users = 'N/A'
                    bots = 'N/A'
                    vcs = 'N/A'

                    r_json = r.json()
                    # log.debug(r_json)
                    if r.status_code == 200 and r_json != {}:
                        r_guilds = len(tls.remove_duplicates([y for x in r_json['discord'] for y in r_json['discord'][x]['guilds']]))
                        if r_guilds > 0: guilds = r_guilds
                        r_users = len(tls.remove_duplicates([y for x in r_json['discord'] for y in r_json['discord'][x]['users']]))
                        if r_users > 0: users = r_users
                        r_bots = len(r_json['discord'])
                        if r_bots > 0: bots = r_bots

                    listeners = [name for y in self.bot.cogs for name, func in self.bot.get_cog(y).get_listeners()]

                    # embed = tls.Embed(ctx, title='Uptime:', description=r_json['uptime'], timestamp=True)
                    embed = tls.Embed(timestamp=True)
                    embed.add_field(name=f'Discord: ', value=f'{round(self.bot.latency * 1000)}ms')
                    embed.add_field(name=f'Ping: ', value=f'{ping}ms')
                    embed.add_field(name=f'API: ', value=f'{api_ping}ms')

                    embed.add_field(name=f'Uptime: ', value=r_json['uptime'], inline=False)

                    embed.add_field(name=f'Bots: ', value=str(bots))
                    embed.add_field(name=f'Members: ', value=ctx.guild.member_count)
                    embed.add_field(name=f'Guilds: ', value=str(guilds))
                    embed.add_field(name=f'Users: ', value=str(users))
                    embed.add_field(name=f'Commands: ', value=str(len(self.bot.commands)))
                    embed.add_field(name=f'Cogs: ', value=str(len(self.bot.cogs)))
                    embed.add_field(name=f'Extensions: ', value=str(len(self.bot.extensions)))
                    embed.add_field(name=f'Listeners: ', value=str(len(listeners)))
                    embed.add_field(name=f'Voice Clients: ', value=str(vcs))

                    embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                    await msg.edit(content='Here is the current status:', embed=embed)

                except Exception as exc:
                    await tls.Message.modify(msg, exc, content='An exception occured. Please try again later.')
                    log.exception(exc)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await update(self)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        await update(self)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await update(self)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await update(self)

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     await update(self)

    @commands.Cog.listener()
    async def on_ready(self):
        # await asyncio.sleep(2)
        await update(self)


def setup(bot):
    bot.add_cog(Core(bot))


async def update(self):
    users = [x.id for x in self.bot.users]
    guilds = [x.id for x in self.bot.guilds]
    voices = len([x.voice_client for x in self.bot.guilds if x.voice_client is not None])

    send = {
        'discord': {
            self.bot.user.id: {
                'name': self.bot.user.name,
                'guilds': guilds,
                'users': users,
                'voices': voices
            }
        }
    }

    # host = json.orm['api']
    await web.api('stat').async_post(send)
    # await web.Client(f"http://{host['host']}:{host['port']}/stat/").async_post(send)
