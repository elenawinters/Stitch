import discord
from discord.ext import commands
from core.logger import log
import core.bot.tools
import core.bot.time
# import core.checks
import core.json
import core.web
import asyncio
import httpx
import time


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
    @core.checks.is_banned()
    async def status(self, ctx):
        """Reveal stats about the Discord and the bot"""
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                # Ping
                before = time.monotonic()
                msg = await ctx.send('Grabbing status...')
                ping = round((time.monotonic() - before) * 1000)

                host = core.json.json.orm['api']
                r = await core.web.Client(f"http://{host['host']}:{host['port']}/stat/").async_get()

                guilds = 'N/A'
                users = 'N/A'
                bots = 'N/A'
                vcs = 'N/A'

                if r.status_code == 200 and r.json() != {}:
                    t = r.json()
                    guilds = len(core.bot.tools.remove_duplicates([z for x in t for z in t[x]['guilds']]))
                    users = len(core.bot.tools.remove_duplicates([z for x in t for z in t[x]['users']]))
                    bots = len(t)

                listeners = []
                for y in self.bot.cogs:  # listeners
                    cog = self.bot.get_cog(y)
                    for name, func in cog.get_listeners():
                        listeners.append(name)

                embed = core.bot.tools.tls.Embed(ctx, title='Uptime:', description=core.bot.time.time.uptime(core.bot.time.time()), timestamp=True)
                embed.add_field(name=f'Bots: ', value=str(bots))
                embed.add_field(name=f'Members: ', value=ctx.guild.member_count)
                embed.add_field(name=f'Guilds: ', value=str(guilds))  # Flagged
                embed.add_field(name=f'Users: ', value=str(users))  # Flagged
                embed.add_field(name=f'Ping: ', value=f'{ping}ms')
                embed.add_field(name=f'Commands: ', value=str(len(self.bot.commands)))
                embed.add_field(name=f'Cogs: ', value=str(len(self.bot.cogs)))
                embed.add_field(name=f'Extensions: ', value=str(len(self.bot.extensions)))
                embed.add_field(name=f'Listeners: ', value=str(len(listeners)))
                # if vcs == 1:  # Flagged
                #     embed.add_field(name=f'Voices: ', value=f'{vcs} client')
                # else:
                #     embed.add_field(name=f'Voices: ', value=f'{vcs} clients')
                embed.set_footer(text=f'Latency of {round(self.bot.latency * 1000)}ms', icon_url=self.bot.user.avatar_url)
                await msg.edit(content='Here is the current status:', embed=embed)

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
        self.bot.user.id: {
            'name': self.bot.user.name,
            'guilds': guilds,
            'users': users,
            'voices': voices
        }
    }

    host = core.json.json.orm['api']
    await core.web.Client(f"http://{host['host']}:{host['port']}/stat/post").async_post(send)
