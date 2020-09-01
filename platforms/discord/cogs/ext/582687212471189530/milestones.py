import discord
from discord.ext import commands
from core.bot.tools import tls
from core.bot.time import time
from core.logger import log
triggered = False


class Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        milestones = [100, 250, 500, 1000, 2500, 5000]
        if member.guild.member_count in milestones:
            log.info(f'{member.guild.member_count}th member: {member.id}')
            embed_json = str({
                "embed": {
                    "author": {
                        "name": self.bot.user.name,
                        "icon_url": self.bot.user.avatar_url
                    },
                    "title": f"Congratulations {member.guild.owner.name}!",
                    "description": f"Your Discord server has reached {member.guild.member_count} members!",
                    "thumbnail": {
                        "url": "https://cdn.discordapp.com/emojis/664504948813463575.png"
                    },
                    "footer": {
                        "text": f"{member.name} is the {member.guild.member_count}th member!",
                        "icon_url": member.avatar_url
                    },
                    "color": 15277653
                }
            })
            embed = tls.Embed.parse(None, embed_json)
            try:
                member.guild.system_channel.send(embed=embed)
            except Exception:
                pass
            # self.bot.unload_extension('cogs.ext.582687212471189530.milestones')


def setup(bot):
    bot.add_cog(Ext(bot))
