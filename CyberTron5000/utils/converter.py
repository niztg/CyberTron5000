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


class RTFSObject(commands.Converter):
    async def convert(self, ctx, argument):
        items = ['discord.', 'commands.', 'utils.']
        for word in items:
            if argument.startswith(word):
                return argument[len(word):]
        return argument


class Prefix(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in ("<@350349365937700864>", "<@!350349365937700864>"):
            raise commands.BadArgument(f"that prefix is reserved!")
        if len(argument) > 15:
            raise commands.BadArgument(f"that prefix is too long! The maximum is **{15}** characters.") # big brain
        return argument