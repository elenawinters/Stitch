import discord
from discord.ext import commands
from func import funcs
from func import perms


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ban', 'hban'])
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, snowflake, *, reason='User was hackbanned'):
        class SnowFake:  # Fake an ABC.Snowflake
            id = snowflake
        try:
            await ctx.guild.ban(SnowFake, delete_message_days=0, reason=reason)
            await ctx.send(f'Hackbanned `{snowflake}` with reason `{reason}`.')
        except discord.Forbidden as err:
            await funcs.respond(ctx, err)
        except discord.HTTPException as err:
            await funcs.respond(ctx, err)
        except Exception as err:
            print(err)

    # # To globally ban an account.
    # @commands.command()
    # @commands.is_owner()
    # async def globalban(self, ctx, snowflake):
    #     pass


def setup(bot):
    bot.add_cog(Moderation(bot))
