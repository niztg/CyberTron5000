from datetime import datetime as dt

import aiogoogletrans
import aiowiki
import async_cleverbot
import async_cse
import discord
from discord.ext import commands, flags

from CyberTron5000.utils import (
    paginator,
    cyberformat,
    converter
)
from CyberTron5000.utils.lists import (
    STAT_NAMES,
    TYPES
)


# ≫

async def fetch_rtfs(res):
    items = []
    for item in res:
        item.pop("module")
        if item not in items:
            items.append(item)
        else:
            continue
    data = []
    for item in items:
        if not item['parent']:
            data.append(f"[`{item['object']}`]({item['url']})")
        else:
            data.append(f"[`{item['parent']}.{item['object']}`]({item['url']})")
    return data


class Api(commands.Cog):
    """Interact with various API's"""

    def __init__(self, bot):
        self.bot = bot
        self.pypi_logo = "https://static1.squarespace.com/static/59481d6bb8a79b8f7c70ec19/594a49e202d7bcca9e61fe23/59b2ee34914e6b6d89b9241c/1506011023937/pypi_logo.png?format=1000w"
        self.clever = async_cleverbot.Cleverbot(bot.config.cleverbot)
        self.clever.set_context(async_cleverbot.DictContext(self.bot))

    @commands.command(aliases=['ily'], help="compliment your friends :heart:")
    async def compliment(self, ctx, *, user=None):
        user = user or ctx.author.mention
        async with self.bot.session.get('https://complimentr.com/api') as r:
            data = await r.json()
        return await ctx.send(f":heart: **{user}, {data['compliment']}**")

    @flags.add_flag("--unit", type=str, default='c')
    @flags.command(usage='<city>,[country]')
    async def weather(self, ctx, city, **flags):
        """
        Shows the weather in your city.
        If you want the temperature to display in farenheit, add `-unit f` at the end of your command usage.
        If you want kelvin, add `-unit k` at the end. (Celsius is the default)
        """
        try:
            async with self.bot.session.get(f"http://api.openweathermap.org/data/2.5/weather?appid={self.bot.config.weather}&q={city}") as r:
                data = await r.json()
            unit = flags.get('unit')
            if not str(unit).startswith(('c', 'k', 'f')):
                return await ctx.send(
                    f"**{unit}** is an invalid unit! Please make sure your unit starts with either **c**, **k** or **f**")
            embed = discord.Embed(colour=self.bot.colour)
            temperature = round(cyberformat.get_temperature(data['main']['temp'], unit), 1)
            feels_like = round(cyberformat.get_temperature(data['main']['feels_like'], unit), 1)
            embed.title = data['name']
            weather = data['weather'][0]
            sunrise = dt.utcfromtimestamp(data['sys']['sunrise']).strftime("%I:%M %p")
            sunset = dt.utcfromtimestamp(data['sys']['sunset']).strftime("%I:%M %p")
            embed.description = f"**{weather['main'].title()}** - {weather['description'].capitalize()}\n"
            embed.description += f"<:temperature:742933558221340723> **{temperature}**° {unit[:1].capitalize()} (Feels Like **{feels_like}**° {unit[:1].capitalize()})\n"
            embed.description += f"☀️ Sunrise: **{sunrise}** UTC • Sunset: **{sunset}** UTC"
            embed.set_thumbnail(url="https://i.dlpng.com/static/png/6552264_preview.png")
            await ctx.send(embed=embed)
        except IndexError:
            raise commands.BadArgument('city not found!')

    @commands.command(help="Shows you info about a Pokémon", aliases=['pokemon', 'poke', 'pokémon', 'pokédex'])
    async def pokedex(self, ctx, pokemon):
        async with self.bot.session.get(f"https://some-random-api.ml/pokedex?pokemon={pokemon.lower()}") as r:
            data = await r.json()
        if r.status != 200:
            raise commands.BadArgument(f'Pokémon **{pokemon}** not found!')
        embed = discord.Embed(title=f"{data['name'].title()} • #{data['id']}", colour=self.bot.colour)
        embed.set_author(name=f'The {" ".join(data["species"])}')
        embed.set_thumbnail(url=data['sprites']['normal'])
        evo_line = []
        for e in data['family']['evolutionLine']:
            if str(e).lower() == pokemon.lower():
                evo_line.append(f"**{e}**")
            else:
                evo_line.append(e)
        n = '\n'
        embed.description = f" ".join([TYPES[item.lower()] for item in data['type']])
        embed.description += f'\n<:pokeball:715599637079130202> {data["description"]}\n**{data["height"]}**\n**{data["weight"]}**'
        embed.add_field(name='Evolution Line',
                        value=f'{" → ".join(evo_line)}' or "**{0}**".format(str(pokemon).capitalize()),
                        inline=False)
        embed.add_field(name='Abilities', value='**' + ', '.join([f'{i}' for i in data['abilities']]) + '**',
                        inline=False)
        embed.add_field(name='Base Stats',
                        value=f"{f'{n}'.join([f'**{STAT_NAMES[key]}:** `{value}`' for key, value in data['stats'].items()])}",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(help="Urban Dictionary", aliases=['urban', 'define', 'def'])
    @commands.is_nsfw()
    async def urbandict(self, ctx, *, terms):
        embeds = []
        try:
            async with self.bot.session.get(f"http://api.urbandictionary.com/v0/define", params={'term': terms}) as r:
                data = await r.json()
            items = data['list']
            for item in items:
                embed = discord.Embed(color=self.bot.colour)
                embed.title = item['word']
                embed.set_author(name=item['author'],
                                 icon_url="https://images-ext-1.discordapp.net/external/Gp2DBilGEcbI2YR0qkOGVkivomBLwmkW_7v3K8cD1mg/https/cdn.discordapp.com/emojis/734991429843157042.png")
                embed.description = cyberformat.hyper_replace(str(item['definition']), old=['[', ']'], new=['', ''])
                embed.description += f"\n👍 **{item['thumbs_up']:,}** 👎 **{item['thumbs_down']}**"
                embed.add_field(name="Example",
                                value=cyberformat.hyper_replace(str(item['example']), old=['[', ']'], new=['', '']))
                embeds.append(embed)
            source = paginator.EmbedSource(embeds)
            menu = paginator.CatchAllMenu(source=source)
            menu.add_info_fields({"<:author:734991429843157042>": "The author of the post", ":thumbsup:": "How many thumbs up the post has", ":thumbsdown:": "How many thumbs down the post has"})
            await menu.start(ctx)
        except IndexError:
            raise commands.BadArgument(f"term not found on urban dictionary.")

    @commands.command(aliases=['wiki'])
    async def wikipedia(self, ctx, *, search):
        embeds = []
        async with ctx.typing():
            wiki = aiowiki.Wiki.wikipedia()
            for page in (await wiki.opensearch(search)):
                embed = discord.Embed(colour=self.bot.colour)
                embed.title = page.title
                embed.url = (await page.urls())[0].split("(")[0]
                embed.description = (await page.summary())[:2000] + "..."
                embeds.append(embed)
        source = paginator.EmbedSource(embeds)
        await paginator.CatchAllMenu(source).start(ctx)

    @commands.command()
    async def fact(self, ctx):
        """Random fact"""
        async with self.bot.session.get(f"https://useless-facts.sameerkumar.website/api") as r:
            data = await r.json()
        await ctx.send(data['data'])

    @commands.command()
    async def pypi(self, ctx, *, package):
        """Shows info on a PyPi package"""
        async with self.bot.session.get(f"https://pypi.org/pypi/{package}/json") as r:
            res = await r.json()
        if r.status != 200:
            raise commands.BadArgument(f'package **{package}** not found!')
        embed = discord.Embed(colour=self.bot.colour)
        char = '\u200b' if not res['info']['author_email'] else f' • {res["info"]["author_email"]}'
        embed.title = f"`pip install {res['info']['name']}=={res['info']['version']}`"
        embed.description = f"{res['info']['summary']}\n"
        embed.set_thumbnail(url=self.pypi_logo)
        if res['info']['requires_python']:
            versions = res['info']['requires_python'].replace("*", "").split(",")
        else:
            versions = ['???']
        embed.description += f"<:author:734991429843157042> **{res['info']['author']}{char}**\n<:python:706850228652998667> {', '.join([f'**{version}**' for version in versions])}\n<:license:737733205645590639> **{res['info']['license'] or '???'}**\n<:releases:734994325020213248> **{len(res['releases'])}**"
        embed.description += f"\n[PyPi Page]({res['info']['project_url']})"
        if res['info']['project_urls']:
            for key, value in res['info']['project_urls'].items():
                embed.description += f"\n[{key.title()}]({value})"
        await ctx.send(embed=embed)

    @commands.command(aliases=['cb'])
    async def cleverbot(self, ctx, *, text: str):
        """
        Ask the clever bot a question.
        """
        async with ctx.typing():
            if len(ctx.message.content) < 2 or len(ctx.message.content) > 60:
                return await ctx.send(
                    f"**{ctx.author.name}**, text must be below 60 characters and over 2.")
            resp = await self.clever.ask(text, ctx.author.id)
            r = str(resp) if str(resp).startswith("I") else cyberformat.minimalize(str(resp))
            if str(r)[-1] not in ['.', '?', '!']:
                suff = "?" if any(s in str(r) for s in ['who', 'what', 'when', 'where', 'why', 'how']) else "."
            else:
                suff = "\u200b"
            send = cyberformat.hyper_replace(str(r), old=[' i ', "i'm", "i'll"], new=[' I ', "I'm", "I'll"])
            await ctx.send(f"**{ctx.author.name}**, {send}{suff}")

    @commands.group(invoke_without_command=True, aliases=['trans'])
    async def translate(self, ctx, *, message):
        translator = aiogoogletrans.Translator()
        res = await translator.translate(message)
        from_lang = aiogoogletrans.LANGUAGES[res.src]
        to_lang = aiogoogletrans.LANGUAGES[res.dest]
        embed = discord.Embed(colour=self.bot.colour,
                              description=f"**{from_lang.title()}**\n{message}\n\n**{to_lang.title()}**\n{res.text}\n\n**Pronunciation**\n{res.pronunciation}").set_author(
            name='Translated Text',
            icon_url="https://cdn3.iconfinder.com/data/icons/google-suits-1/32/18_google_translate_text_language_translation-512.png")
        return await ctx.send(embed=embed.set_footer(text=f"{round(res.confidence * 100)}% confident"))

    @translate.command(name='to', invoke_without_command=True)
    async def to(self, ctx, target_lang, *, message):
        translator = aiogoogletrans.Translator()
        try:
            res = await translator.translate(message, dest=target_lang)
        except ValueError:
            return await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, `{target_lang}` is not a valid langauge!")
        from_lang = aiogoogletrans.LANGUAGES[res.src]
        to_lang = aiogoogletrans.LANGUAGES[res.dest]
        embed = discord.Embed(colour=self.bot.colour,
                              description=f"**{from_lang.capitalize()}**\n{message}\n\n**{to_lang.capitalize()}**\n{res.text}\n\n**Pronunciation**\n{res.pronunciation}").set_author(
            name='Translated Text',
            icon_url="https://cdn3.iconfinder.com/data/icons/google-suits-1/32/18_google_translate_text_language_translation-512.png")
        return await ctx.send(embed=embed.set_footer(text=f"{res.confidence * 100}% confident"))

    @commands.command(aliases=['g'])
    async def google(self, ctx, *, query=None):
        """Shows you google search results for a specified query"""
        client = async_cse.Search(self.bot.config.google_key)
        results = await client.search(query, safesearch=not (ctx.channel.is_nsfw()))
        embeds = []
        for res in results:
            embeds.append(
                discord.Embed(colour=self.bot.colour, title=res.title, description=res.description, url=res.url))
        source = paginator.EmbedSource(embeds)
        await client.close()
        await paginator.CatchAllMenu(source=source).start(ctx)

    @commands.command()
    async def rtfs(self, ctx, *, query: converter.RTFSObject):
        """Shows results from. the discord.py sourcecode"""
        async with self.bot.session.get(f"https://rtfs.eviee.me/dpy?search={query}") as r:
            res = await r.json()
        if not res:
            return await ctx.send("No results.")
        embed = discord.Embed(color=self.bot.colour)
        data = await fetch_rtfs(res)
        source = paginator.IndexedListSource(data, embed=embed, per_page=5, show_index=False)
        await paginator.CatchAllMenu(source=source).start(ctx)

    @commands.command(aliases=['gif'])
    @commands.is_nsfw()
    async def giphy(self, ctx, *, query):
        """Get a random gif based on your query"""
        async with self.bot.session.get('http://api.giphy.com/v1/gifs/search?q=' + query + f'&api_key={self.bot.config.giphy}&limit=10') as r:
            res = await r.json()
        data = res.get('data')
        embeds = []
        for item in data:
            embed = discord.Embed(colour=self.bot.colour, title=f"> {item.get('title')}")
            embed.set_thumbnail(url='https://image.ibb.co/b0Gkwo/Poweredby_640px_Black_Vert_Text.png')
            embed.set_image(url=item.get('images')['original']['url'])
            embeds.append(embed)
        source = paginator.EmbedSource(embeds)
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)


def setup(bot):
    bot.add_cog(Api(bot))
