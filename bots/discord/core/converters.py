import discord

""" Nadeko = Leovoel
    plainText = content
    . = .embed
    thumbnail = .embed.thumbnail.url
    image = .embed.image.url
"""


class DiscordEmbed:  # references guilds.pyw
    def __init__(self, data: dict):
        self.data = data

    def nadeko2leovoel(self) -> dict:  # Stitch uses the leovoel format
        temp = {}
        temp['embed'] = self.data
        pass

    def leovoel2embed(self):
        if bot is None:  # R-Filter needs to be reworked. Doesn't
            # work in private chats, even when it really should.
            try:
                replaced = rfilterm(ctx.author, string, ctx.bot, ctx.guild.id)
            except Exception:
                replaced = string
        else:
            try:
                replaced = rfilterm(ctx.author, string, bot, ctx.guild.id)
            except Exception:
                try:
                    replaced = rfilterm(ctx, string, bot, ctx.guild.id)
                except Exception:
                    replaced = string
        # JSON -> Dict
        try:
            try:
                import ast
                literal = ast.literal_eval(replaced)
            except Exception:  # If json function fails,
                # it'll output the error for it instead
                # of the ast.literal_eval error.
                import json
                literal = json.loads(replaced)
        except Exception:
            literal = dict(string)
        message = None
        if 'embed' in literal:
            try:
                message = literal['content']
            except KeyError:
                pass
            literal = literal['embed']
        if 'timestamp' in literal:
            if literal['timestamp'] == '0000-00-00T00:00:00Z':
                literal['timestamp'] = time.Now()
            else:
                literal['timestamp'] = time.Parse.iso(literal['timestamp'])
        if 'color' in literal:
            if literal['color'] < 0:
                try:
                    literal['color'] = get_color(bot, ctx.author).value
                except Exception:
                    literal['color'] = 0
        embed = discord.Embed.from_dict(literal)
        return embed, message
        pass
