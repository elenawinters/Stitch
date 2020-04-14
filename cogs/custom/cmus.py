import discord
from discord.ext import commands
from core.bot.tools import tls
from core.color import trace
from core.logger import log
from core.ext import assets
import youtube_dl
import functools
import traceback
import requests
import asyncio
import random


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url=None):
        if await Player.can_connect(ctx, False):
            await Player.join(ctx.message.author)
        if Player.is_connected(ctx):
            try:
                if url is not None:
                    async with ctx.typing():
                        info, data = await Player.info(url, loop=self.bot.loop, ctx=ctx)
                        # log.debug(info)
                        if info is not None:
                            if len(info) > 1:
                                playlist = data['title']
                            else:
                                playlist = None
                            embed = tls.Embed(ctx)
                            for item in info:  # Append tracks to queue. Eventually it'll just be pfp and data.
                                try:
                                    item.update({'discord_mention': ctx.author.mention})
                                    extractor = Player.Extractor.fetch(data)
                                    queue[ctx.guild.id]['q'].append(item)
                                    # log.debug(item)
                                except KeyError as err:
                                    log.error(err)
                                    # break
                            if playlist is None:
                                item = await Player.process_picture(item, extractor[0])
                                try:
                                    # log.debug(queue[ctx.guild.id]['q'][-1]['extractor'])
                                    embed.set_author(name=item['uploader'], url=item['uploader_url'], icon_url=queue[ctx.guild.id]['q'][-1]['pfp'])
                                except KeyError as err:
                                    embed.set_author(name=item['uploader'], icon_url=queue[ctx.guild.id]['q'][-1]['pfp'])
                                embed.add_field(name=f"{item['title']}", value=f"has been added to the queue.", inline=False)
                            else:
                                embed.add_field(name=f"{len(info)} tracks added from", value=f" playlist **{playlist}**", inline=False)
                            await ctx.send(embed=embed)

                else:  # If no URL specified, try to resume
                    Player.resume(ctx)

                await Player.loop(self, ctx)

            except Exception as err:
                random.seed(traceback.format_exc())
                number = random.randint(10000, 99999)
                await ctx.send(f'Oops! Something went wrong! `(#{number})`')
                log.exception(f'Code #{number}', exc_info=err)

    @commands.group(aliases=['q'])
    async def queue(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                if queue[ctx.guild.id]['playing']:  # If object exists in here, we show the queue
                    embed = tls.Embed(ctx, description=f"Currently {(len(queue[ctx.guild.id]['q']) + 1)} songs in queue")
                    curr = queue[ctx.guild.id]['playing'][0]
                    try:
                        embed.add_field(name=f"**>**[**1**] {curr['title']}", value=f"**Artist:** {curr['author']}", inline=False)
                    except Exception:
                        embed.add_field(name=f"**>**[**1**] {curr['title']}", value=f"**Added by:** {curr['discord_mention']}", inline=False)
                    pos = 2
                    for song in queue[ctx.guild.id]['q']:
                        if pos <= 10:
                            try:
                                embed.add_field(name=f"[**{pos}**] {song['title']}", value=f"**Artist:** {song['author']}", inline=False)
                            except Exception:
                                embed.add_field(name=f"[**{pos}**] {song['title']}", value=f"**Added by:** {song['discord_mention']}", inline=False)
                        pos += 1
                    if pos > 10:
                        dif = (len(queue[ctx.guild.id]['q']) + 1) - 10
                        embed.set_footer(text=f'Plus {dif} other tracks.', icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('The queue is currently empty.')

            except Exception as err:
                random.seed(traceback.format_exc())
                number = random.randint(10000, 99999)
                await ctx.send(f'Oops! Something went wrong! `(#{number})`')
                log.exception(f'Code #{number}', exc_info=err)

    @queue.command()
    async def backend(self, ctx):
        try:
            log.debug(queue[ctx.guild.id]['playing'][0])
        except Exception:
            log.debug(None)
        log.debug(queue[ctx.guild.id]['q'])

    @queue.command()
    async def clear(self, ctx):
        if Player.is_connected(ctx):
            queue[ctx.guild.id]['q'].clear()
        else:
            await ctx.send('Not connected to voice')

    @queue.command()
    async def remove(self, ctx, loc: int):
        if Player.is_connected(ctx):
            embed = tls.Embed(ctx, description=f"Removed {queue[ctx.guild.id]['q'][loc - 2]['title']} from the queue.")
            try:
                del queue[ctx.guild.id]['q'][loc - 2]
                await ctx.send(embed=embed)
            except IndexError:
                await ctx.send(f'Nothing at index location {loc} exists!')

    @queue.command(aliases=['shuff'])
    async def shuffle(self, ctx):
        if Player.is_connected(ctx):
            random.shuffle(queue[ctx.guild.id]['q'])
            await ctx.send(f"Shuffled {len(queue[ctx.guild.id]['q'])} tracks")

    @queue.command(aliases=['len'])
    async def length(self, ctx):
        await ctx.send(f"Queue currently contains {len(queue[ctx.guild.id]['q'])} tracks")

    @commands.command(aliases=['now_playing', 'nowplaying', 'now-playing', 'now', 'playing'])
    async def np(self, ctx):
        if Player.is_connected(ctx):
            curr = queue[ctx.guild.id]['playing'][0]
            import math
            try:
                desc = curr['description']
                # length = math.sqrt((len(desc))) + 200
                # desc = desc[:int(length)]
                # desc = desc[:248]
                desc = desc[:148]
            except TypeError:
                desc = None
            # TODO: make it filter out newlines
            if desc is not None:
                embed = tls.Embed(ctx, title=curr['title'], description=f'{desc}...')
            else:
                embed = tls.Embed(ctx, title=curr['title'])
            try:
                embed.set_image(url=curr['thumbnail'])
            except KeyError:
                pass
            try:
                embed.set_author(name=curr['uploader'], url=curr['uploader_url'], icon_url=curr['pfp'])
            except KeyError:
                embed.set_author(name=curr['uploader'], icon_url=curr['pfp'])
            if curr['pfp'] != discord.Embed.Empty:
                embed.set_thumbnail(url=curr['pfp'])
            # log.debug(curr['pfp'])
            await ctx.send(embed=embed)

    @commands.command(aliases=['next'])
    async def skip(self, ctx):
        if Player.is_connected(ctx):
            Player.skip(ctx)
            await ctx.send('Skipping the current song')

    @commands.command(aliases=['stop'])
    async def pause(self, ctx):
        if Player.is_connected(ctx):
            await ctx.send('Pausing the player')
            Player.pause(ctx)

    @commands.command()
    async def resume(self, ctx):
        if Player.is_connected(ctx):
            await ctx.send('Resuming the player')
            Player.resume(ctx)

    @commands.command(aliases=['rejoin'])
    async def reconnect(self, ctx):
        if await Player.can_connect(ctx):
            await Player.join(ctx.message.author)
            await Player.loop(self, ctx)

    @commands.command(aliases=['connect'])
    async def join(self, ctx):
        if await Player.can_connect(ctx):
            await Player.join(ctx.message.author)

    @commands.command(aliases=['disconnect'])
    async def leave(self, ctx):
        await Player.disconnect(ctx.me)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member_updated, before, after):
        member = Player.self(self, member_updated)
        if member.voice is not None:
            if len(member.voice.channel.members) == 1:
                if member.voice.channel.members[0].id is self.bot.user.id:
                    await Player.disconnect(member)


def setup(bot):
    bot.add_cog(Music(bot))


class Player:
    @classmethod
    async def connect(cls, member):
        try:
            await member.voice.channel.connect()
        except Exception:
            pass

    @classmethod
    async def disconnect(cls, member, clear=False):
        try:
            await member.guild.voice_client.disconnect()
        except Exception:
            pass
        if clear is True:
            queue.pop(member.guild.id, None)
        # del queue[member.guild.id]

    class Play:
        def __new__(cls, ctx, stream):
            ctx.voice_client.play(stream)

        @classmethod
        def file(cls, sound, member):
            import os
            abspath = os.path.abspath('.')
            path = f'{abspath}\\{sound.value}'
            audio = discord.FFmpegPCMAudio(source=path)
            member.guild.voice_client.play(audio)

    play = Play

    @classmethod
    async def join(cls, member):
        await Player.connect(member)
        # TODO: Find a less annoying sound
        # player.play.file(SoundFiles.connect, member)

    @classmethod
    def pause(cls, member):
        member.guild.voice_client.pause()

    @classmethod
    def resume(cls, member):
        member.guild.voice_client.resume()

    @classmethod
    def skip(cls, member):
        member.guild.voice_client.stop()

    @classmethod
    async def loop(cls, self, ctx):
        if not Player.is_playing(ctx) and not Player.is_paused(ctx) and len(queue[ctx.guild.id]['q']) > 0:
            while Player.has_queue(ctx):
                if not Player.is_playing(ctx) and not Player.is_paused(ctx):
                    try:
                        try:
                            url = queue[ctx.guild.id]['q'][0]['webpage_url']
                        except Exception:
                            url = queue[ctx.guild.id]['q'][0]['id']
                        stream = await YTDLSource.create_source(url=url, loop=self.bot.loop)
                        Player.play(ctx, stream)
                        new = queue[ctx.guild.id]['q'].pop(0)
                        if 'ie_key' in new:  # if Playlist object
                            if new['ie_key'].lower() == 'youtube':
                                added_by = new['discord_mention']
                                data_trunk, new = await Player.info(new['id'], loop=self.bot.loop, ctx=ctx)
                                # new = new[0]  # Format into usable form
                                new.update({'discord_mention': added_by})
                        extractor = Player.Extractor.fetch(new)
                        new = await Player.process_picture(new, extractor)
                        # log.debug(new)
                        queue[ctx.guild.id]['playing'].insert(0, new)
                        queue[ctx.guild.id]['player'] = stream
                        embed = tls.Embed(ctx, title=new['title'], description='is now playing.')
                        # log.debug(new['pfp'])
                        try:
                            embed.set_author(name=new['uploader'], url=new['uploader_url'], icon_url=new['pfp'])
                        except KeyError as err:
                            embed.set_author(name=new['uploader'], icon_url=new['pfp'])
                        # embed.set_image(url=new['thumbnail'])
                        try:
                            await ctx.send(embed=embed)
                        except Exception as e:
                            log.warn(f'> {e}')
                    except Exception as err:
                        log.debug(f'> {err}')
                        pass
                await asyncio.sleep(4)

    @classmethod
    async def can_connect(cls, ctx, response=True):  # Includes responses if fail
        if not Player.is_connected(ctx):
            if ctx.message.author.voice is not None:
                return True
            else:
                if response:
                    await ctx.send('You are not connected to voice.')
        else:
            if response:
                await ctx.send('Already connected to voice!')
        return False

    @classmethod
    def has_queue(cls, ctx):
        if ctx.me.voice is not None:
            if Player.is_connected(ctx):
                if ctx.guild.voice_client.is_paused() or ctx.guild.voice_client.is_playing() or len(queue[ctx.guild.id]['q']) > 0:
                    return True
        return False

    @classmethod
    def self(cls, self, member):  # Returns member object of bot.
        guild = member.guild
        mem = guild.get_member(self.bot.user.id)
        return mem

    @classmethod
    def is_connected(cls, ctx):  # Is the bot connected to voice?
        if ctx.me.voice is not None:
            try:
                return ctx.guild.voice_client.is_connected()
            except AttributeError:
                return False
        else:
            return False

    @classmethod
    def is_playing(cls, ctx):
        if ctx.me.voice is not None:
            return ctx.guild.voice_client.is_playing()
        else:
            return False

    @classmethod
    def is_paused(cls, ctx):
        if ctx.me.voice is not None:
            return ctx.guild.voice_client.is_paused()
        else:
            return False

    @classmethod
    async def info(cls, inurl, **kwargs):  # VIDEO INFO
        loop = kwargs.get('loop', asyncio.get_event_loop())
        do_log = kwargs.get('log', False)
        ctx = kwargs.get('ctx', None)
        from core.bot.funcs import respond
        url = inurl
        # if inurl.casefold() in MusicTests.__members__.keys():
        #     url = MusicTests[inurl.casefold()].value
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False, process=False))
            # log.debug(data)
        except Exception as err:
            if ctx is not None:
                await respond(ctx, err, url)
            data = {}

        if do_log:
            log.debug(data)
        if 'extractor_key' in data:
            if data['extractor_key'] == 'YoutubeSearch':
                return None, None
            else:
                if 'entries' in data:
                    count = 0
                    entries = []
                    for x in data['entries']:  # Don't add to output
                        if not x['title'] == '[Deleted video]' or x['title'] == '[Private video]':
                            entries.append(x)
                        if count >= 1000:
                            break
                        count += 1
                    return entries, data
                else:
                    # log.debug(data)
                    return [data], data
        else:
            return None, None

    @classmethod
    async def process_picture(cls, _dict, platform):
        if 'channel_id' in _dict:  # Get profile picture
            pfp = await Player.profile_picture(_dict['channel_id'], platform)
        else:
            pfp = await Player.profile_picture(_dict['uploader_id'], platform)
        _dict.update({'pfp': pfp})
        return _dict

    @classmethod
    async def profile_picture(cls, _id, extractor='youtube'):
        from core.bot.tools import crypt
        from data.data import data
        from core import json
        # print(_id)
        # print(extractor)
        # log.debug(extractor)
        info = data.base['cache'].find_one(id=_id, platform=extractor)
        # print(info)
        try:
            if info is None:
                if extractor == 'youtube':  # 2 points
                    base = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={_id}&key={crypt(json.json.orm['secure']['extractors'][extractor])}"
                    info = requests.get(base).json()['items'][0]['snippet']['thumbnails']['high']['url']
                    # log.debug(info)
                    data.base['cache'].upsert(dict(platform=extractor, id=_id, data=info), ['id'])
                elif extractor == 'twitch':  # Kraken - Depreciated.
                    version = 'kraken'
                    if version == 'kraken':  # Kraken implementation
                        import aiohttp
                        session = aiohttp.ClientSession()
                        url = "https://api.twitch.tv/kraken/users?login=" + _id
                        header = {
                            'Client-ID': crypt(json.json.orm['secure']['extractors']['twitch']),
                            'Accept': 'application/vnd.twitchtv.v5+json'
                        }
                        async with session.get(url, headers=header) as r:
                            _data = await r.json(encoding='utf-8')
                        await session.close()
                        if r.status == 200:
                            if _data['users']:
                                info = _data['users'][0]['logo']
                        data.base['cache'].upsert(dict(platform=extractor, id=_id, data=info), ['id'])
                    elif version == 'helix':  # No implementation
                        return discord.Embed.Empty
                else:
                    return discord.Embed.Empty
            else:
                info = info['data']
                pass
        except Exception as err:
            random.seed(traceback.format_exc())
            number = random.randint(10000, 99999)
            log.exception(f'Code #{number}', exc_info=err)
            info = assets.Discord.error.value
        # log.debug(info)
        return info

    class Extractor:
        @classmethod
        def fetch(cls, data):
            if 'extractor' in data:
                keys = data['extractor'].split(':')
                extractor = keys[0].lower()
                sub = None
                sort = None
                if len(keys) > 1:
                    sub = keys[1].lower()
                    if len(keys) > 2:
                        sort = keys[2].lower()

                return extractor, sub, sort
            elif 'ie_key' in data:
                extractor = data['ie_key'].lower()
                return extractor, None, None
            else:
                return None, None, None


class Queue(dict):  # Queue system
    def __getitem__(self, key):
        if key not in self.__dict__:
            self.__dict__[key] = {'player': None, 'q': [], 'playing': []}
        return self.__dict__[key]


class LoggerHook(object):
    def debug(self, msg):
        # log.debug(msg)
        pass

    def warning(self, msg):
        # log.warning(msg)
        pass

    def error(self, msg):
        log.error(msg)


queue = Queue()
options = {
    'logger': LoggerHook(),
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True
}

ytdl = youtube_dl.YoutubeDL(options)  # The following is taken from the basic_voice.py example on the discord.py github.


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def create_source(cls, url, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        func = functools.partial(ytdl.extract_info, url, download=download)
        data = await loop.run_in_executor(None, func)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        if download:
            source = ytdl.prepare_filename(data)
        else:
            source = data['url']
        return cls(discord.FFmpegPCMAudio(source, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', options='-loglevel 0'), data=data)
