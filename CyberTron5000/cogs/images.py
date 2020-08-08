import json

import aiohttp
import discord
from discord.ext import commands

from CyberTron5000.utils.converter import ImageConverter

member_converter = commands.MemberConverter()
emoji_converter = commands.EmojiConverter()


def dagpi():
    with open("json_files/secrets.json", "r") as f:
        res = json.load(f)
    return res['dagpi_token']


dagpi_token = dagpi()


class Images(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tick = ":tickgreen:732660186560462958"
        self.daggy = 491174779278065689

    @commands.command()
    async def wanted(self, ctx, *, url: ImageConverter = None):
        """
        Wanted...
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': url}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/wanted', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def obama(self, ctx, *, url: ImageConverter = None):
        """
        I'm just great.
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': url}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/obamameme', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def bad(self, ctx, *, url: ImageConverter = None):
        """
        Bad boy! Bad boy!
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': url}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/bad', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def hitler(self, ctx, *, url: ImageConverter = None):
        """
        What a monster
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': url}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/hitler', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def tweet(self, ctx, url: discord.Member, *, tweet: str):
        """
        Yeah i use twitter
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        image = str(url.avatar_url_as(static_format='png')) or str(ctx.author.avatar_url_as(static_format='png'))
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': image, 'text': tweet, 'name': url.display_name}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/tweet', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def quote(self, ctx, member: discord.Member, *, quote: str):
        """
        'Stop believing internet quotes' - God
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': str(member.avatar_url_as(static_format='png')),
                    'text': quote, 'name': member.display_name}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/quote', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def triggered(self, ctx, *, url: ImageConverter = None):
        """
        Brrrr
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': url}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/triggered', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def gay(self, ctx, *, url: ImageConverter = None):
        """
        :rainbow_flag:
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': url}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/gay', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def paint(self, ctx, *, url: ImageConverter = None):
        """
        Paint a masterpiece
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        if not url:
            if ctx.message.attachments:
                url = str(ctx.message.attachments[0].url)
            else:
                url = str(ctx.author.avatar_url_as(static_format='png'))
        else:
            url = url
        async with ctx.typing():
            resp = {'token': dagpi_token, 'url': url}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/paint', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def whyareyougay(self, ctx, url: ImageConverter, url2: ImageConverter):
        """
        Why are you gay?
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
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
            resp = {'token': dagpi_token, 'url2': url, 'url': url2}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/whyareyougay', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def fiveguys(self, ctx, url: ImageConverter, url2: ImageConverter):
        """
        uwu
        """
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
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
            resp = {'token': dagpi_token, 'url': url, 'url2': url2}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/5g1g', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Images(client))
