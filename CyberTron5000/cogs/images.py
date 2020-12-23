import discord
from discord.ext import commands

from CyberTron5000.utils.converter import ImageConverter

member_converter = commands.MemberConverter()
emoji_converter = commands.EmojiConverter()


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def daggy(self):
        return self.bot.get_user(491174779278065689)

    @property
    def dagpi_token(self):
        return self.bot.config.dagpi_token

    async def get_dagpi(self, opt):
        pass

def setup(bot):
    bot.add_cog(Images(bot))
