from contextlib import suppress

from discord.ext import commands
from validator_collection import checkers

member_converter = commands.MemberConverter()
emoji_converter = commands.EmojiConverter()


class ImageConverter(commands.Converter):
    """Huge thanks to Daggy1234 for making this converter!"""
    async def convert(self, ctx, argument):
        with suppress(Exception):
            mem = await member_converter.convert(ctx, argument)
            return str(mem.avatar_url_as(static_format='png', size=1024))
        with suppress(Exception):
            emoji = await emoji_converter.convert(ctx, str(argument))
            return str(emoji.url)
        if ctx.message.attachments:
            with suppress(Exception):
                return str(ctx.message.attachments[0].url)
        elif checkers.is_url(str(argument)):
            return str(argument)
        else:
            raise commands.BadArgument()

