import aiohttp
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

    @commands.command(name='wanted')
    async def _static_wanted(self, ctx, *, url: ImageConverter = None):
        """
        Wanted...
        """
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            headers = {'token': self.dagpi_token, 'url': url}
            async with self.bot.session.post('https://dagpi.tk/api/wanted', headers=headers) as r:
                data = await r.json()
            try:
                image = data['url']
            except KeyError:
                return await ctx.send(data.get('error'))
            embed = discord.Embed(colour=self.bot.colour)
            embed.set_image(url=image)
            embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!", icon_url=self.daggy.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='obama')
    async def _static_obama(self, ctx, *, url: ImageConverter = None):
        """
        I'm just great.
        """
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            headers = {'token': self.dagpi_token, 'url': url}
            async with self.bot.session.post('https://dagpi.tk/api/obamameme', headers=headers) as r:
                data = await r.json()
            try:
                image = data['url']
            except KeyError:
                return await ctx.send(data.get('error'))
            embed = discord.Embed(colour=self.bot.colour)
            embed.set_image(url=image)
            embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!", icon_url=self.daggy.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='bad')
    async def _static_bad(self, ctx, *, url: ImageConverter = None):
        """
        Bad boy! Bad boy!
        """
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            headers = {'token': self.dagpi_token, 'url': url}
            async with self.bot.session.post('https://dagpi.tk/api/bad', headers=headers) as r:
                data = await r.json()
            try:
                image = data['url']
            except KeyError:
                return await ctx.send(data.get('error'))
            embed = discord.Embed(colour=self.bot.colour)
            embed.set_image(url=image)
            embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!", icon_url=self.daggy.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='hitler')
    async def _static_hitler(self, ctx, *, url: ImageConverter = None):
        """
        What a monster
        """
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            headers = {'token': self.dagpi_token, 'url': url}
            async with self.bot.session.post('https://dagpi.tk/api/hitler', headers=headers) as r:
                data = await r.json()
            try:
                image = data['url']
            except KeyError:
                return await ctx.send(data.get('error'))
            embed = discord.Embed(colour=self.bot.colour)
            embed.set_image(url=image)
            embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!", icon_url=self.daggy.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def tweet(self, ctx, url: discord.Member, *, tweet: str):
        """
        Yeah i use twitter
        """
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            headers = {'token': self.dagpi_token, 'url': url, 'text': tweet, 'name': url.display_name}
            async with self.bot.session.post('https://dagpi.tk/api/tweet', headers=headers) as r:
                data = await r.json()
            try:
                image = data['url']
            except KeyError:
                return await ctx.send(data.get('error'))
            embed = discord.Embed(colour=self.bot.colour)
            embed.set_image(url=image)
            embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!", icon_url=self.daggy.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def quote(self, ctx, member: discord.Member, *, quote: str):
        """
        'Stop believing internet quotes' - Abraham Lincoln
        """
        async with ctx.typing():
            headers = {'token': self.dagpi_token, 'url': str(member.avatar_url_as(static_fornat='png')), 'text': quote,
                       'name': member.display_name}
            async with self.bot.session.post('https://dagpi.tk/api/quote', headers=headers) as r:
                data = await r.json()
            try:
                image = data['url']
            except KeyError:
                return await ctx.send(data.get('error'))
            embed = discord.Embed(colour=self.bot.colour)
            embed.set_image(url=image)
            embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!", icon_url=self.daggy.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def triggered(self, ctx, *, url: ImageConverter = None):
        """
        Brrrr
        """

        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            headers = {'token': self.dagpi_token, 'url': url}
            async with self.bot.session.post('https://dagpi.tk/api/triggered', headers=headers) as r:
                data = await r.json()
                try:
                    image = data['url']
                except KeyError:
                    return await ctx.send(data.get('error'))
                embed = discord.Embed(colour=self.bot.colour)
                embed.set_image(url=image)
                embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!",
                                 icon_url=self.daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def gay(self, ctx, *, url: ImageConverter = None):
        """
        :rainbow_flag:
        """

        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': self.dagpi_token, 'url': url}
            async with self.bot.session.post('https://dagpi.tk/api/gay', headers=resp) as r:
                data = await r.json()
                try:
                    image = data['url']
                except KeyError:
                    return await ctx.send(data.get('error'))
                embed = discord.Embed(colour=self.bot.colour)
                embed.set_image(url=image)
                embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!",
                                 icon_url=self.daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def paint(self, ctx, *, url: ImageConverter = None):
        """
        Paint a masterpiece
        """

        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': self.dagpi_token, 'url': url}
            async with self.bot.session.post('https://dagpi.tk/api/paint', headers=resp) as r:
                data = await r.json()
                try:
                    image = data['url']
                except KeyError:
                    return await ctx.send(data.get('error'))
                embed = discord.Embed(colour=self.bot.colour)
                embed.set_image(url=image)
                embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!",
                                 icon_url=self.daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def whyareyougay(self, ctx, url: ImageConverter, url2: ImageConverter):
        """
        Why are you gay?
        """

        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        if not url2:
            url2 = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url2 = url2
        async with ctx.typing():
            resp = {'token': self.dagpi_token, 'url2': url, 'url': url2}
            async with self.bot.session.post('https://dagpi.tk/api/whyareyougay', headers=resp) as r:
                data = await r.json()
                try:
                    image = data['url']
                except KeyError:
                    return await ctx.send(data.get('error'))
                embed = discord.Embed(colour=self.bot.colour)
                embed.set_image(url=image)
                embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!",
                                 icon_url=self.daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def fiveguys(self, ctx, url: ImageConverter, url2: ImageConverter):
        """
        uwu
        """

        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        if not url2:
            url2 = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url2 = url2
        async with ctx.typing():
            resp = {'token': self.dagpi_token, 'url': url, 'url2': url2}
            async with self.bot.session.post('https://dagpi.tk/api/5g1g', headers=resp) as r:
                data = await r.json()
                try:
                    image = data['url']
                except KeyError:
                    return await ctx.send(data.get('error'))
                embed = discord.Embed(colour=self.bot.colour)
                embed.set_image(url=image)
                embed.set_footer(text=f"Much thanks to {str(self.daggy)} for this amazing API!",
                                 icon_url=self.daggy.avatar_url)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))
