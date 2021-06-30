import discord


def find_suitable_channel(guild: discord.Guild):
    if guild is not None:
        if guild.system_channel is not None:
            return guild.system_channel
        else:
            for x in guild.text_channels:
                perms = x.permissions_for(guild.me)
                if perms.read_messages and perms.send_messages and perms.create_instant_invite:
                    return x
