import discord
from discord.ext import commands
from core.bot.tools import split_string
from core.bot.tools import tls
from data.data import data
from core.bot.enums import *
import core.checks


class Reporting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['reports', 'review', 'r'])
    @core.checks.is_banned()  # REEE I HAVE TO FIX THIS
    async def report(self, ctx):
        """Report something to the bot developer.
        .report [text]
        .report view [report number]"""
        if ctx.invoked_subcommand is None:
            args = ctx.message.content.split(' ')
            if len(args) > 1:
                try:
                    report_data = dict(id=ctx.message.id,
                                       serverid=ctx.guild.id,
                                       servername=ctx.guild.name,
                                       features=str(ctx.guild.features),
                                       userid=ctx.author.id,
                                       discordtag=str(ctx.author),
                                       nickname=ctx.author.nick,
                                       report_text=split_string(ctx.message.content, f'{args[0]} '),
                                       timestamp=ctx.message.created_at)
                    rid = data.base['reports'].insert(report_data)

                    try:
                        await ctx.send(f'You have filed your report (#{rid})')
                    except Exception:
                        pass
                except Exception:
                    await ctx.send('Failed to send your report.')
            else:
                raise discord.ext.commands.MissingRequiredArgument(report_content)

    @report.command(aliases=['v'])
    async def view(self, ctx, arg: int = 0):
        if arg >= 0:
            entry = data.base['reports'].find_one(id=arg)
            if entry is not None:
                user = self.bot.get_user(entry['userid'])
                guild = self.bot.get_guild(entry['serverid'])
                embed = tls.embed(ctx, description=f"```{entry['report_text']}```", timestamp=entry['timestamp'])
                embed.set_author(name=f"{user} submitted report #{entry['id']}", icon_url=user.avatar_url)
                embed.add_field(name='Server:', value=f'{guild.name}')
                embed.add_field(name='Reviewed:', value=f"{bool(entry['reviewed'])}")
                if guild.icon is None:
                    embed.set_thumbnail(url=DiscordAvatars.default)
                else:
                    embed.set_thumbnail(url=guild.icon_url)

                await ctx.send(embed=embed)

    @report.command(aliases=['m', 'flag', 'f'])
    @commands.is_owner()
    async def mark(self, ctx, arg: int = 0):
        if arg >= 0:
            entry = data.base['reports'].find_one(id=arg)
            if entry is not None:
                new = not bool(entry['reviewed'])
                data.base['reports'].update(dict(id=arg, reviewed=new), ['id'])
                await ctx.send(f'Updated report #{arg}')


def setup(bot):
    bot.add_cog(Reporting(bot))


class report_content:  # Literally just here for the simulated error thingy.
    name = 'report_content'
