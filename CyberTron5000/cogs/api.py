import datetime
import json
from html import unescape as unes

import aiogoogletrans
import aiohttp
import aiowiki
import async_cleverbot
import async_cse
import discord
from discord.ext import commands

from CyberTron5000.utils import paginator, cyberformat
from CyberTron5000.utils.lists import STAT_NAMES, TYPES


# ≫

def secrets():
    with open("json_files/secrets.json", "r") as f:
        return json.load(f)

token = secrets()

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
    
    def __init__(self, client):
        self.client = client
        self.pypi_logo = "https://static1.squarespace.com/static/59481d6bb8a79b8f7c70ec19/594a49e202d7bcca9e61fe23/59b2ee34914e6b6d89b9241c/1506011023937/pypi_logo.png?format=1000w"
        self.bot = async_cleverbot.Cleverbot(token['cleverbot'])
        self.bot.set_context(async_cleverbot.DictContext(self.bot))
    
    @commands.command(aliases=['ily'], help="compliment your friends :heart:")
    async def compliment(self, ctx, *, user: discord.Member = None):
        try:
            user = user or ctx.message.author
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://complimentr.com/api") as r:
                    comp = await r.json()
                    await cs.close()
            
            await ctx.send(
                embed=discord.Embed(description=f"{user.name}, {unes(comp['compliment'])}",
                                    colour=self.client.colour).set_footer(
                    text="https://complimentr.com/api"))
        except Exception as error:
            await ctx.send(f"```py\n{error}```")
    
    @commands.group(help="Shows the weather in your city.", invoke_without_command=True)
    async def weather(self, ctx, city):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        f"http://api.openweathermap.org/data/2.5/weather?appid=2a5e00144cd0454e62a99f975c701c4e&q={city}") as r:
                    res = await r.json()
                    await cs.close()
                topic = res['weather'][0]
                kelv_temp = round(res['main']['temp'], 1)
                cels_temp = round(kelv_temp - 273.15, 1)
                faren_temp = round(cels_temp * 1.8 + 32, 1)
                ts = res['sys']['sunrise']
                te = res['sys']['sunset']
                town = res['name']
                sunrise = datetime.datetime.fromtimestamp(ts).strftime("%H:%M")
                sunset = datetime.datetime.fromtimestamp(te).strftime("%H:%M")
                embed = discord.Embed(colour=self.client.colour,
                                      description="**" + unes(topic['main']) + "**" + '\n' + unes(
                                          topic['description']).capitalize())
                embed.add_field(name="Info",
                                value=f"*Temperature:* **{cels_temp}**° C • **{faren_temp}**° F • **{kelv_temp}**° K\n*Sunrise:* **{sunrise} UTC**\n*Sunset:* **{sunset} UTC**")
                embed.set_footer(text=f"Weather for {town} • http://api.openweathermap.org")
                await ctx.send(embed=embed)
        except KeyError:
            await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, city probably not found. You can specify even more by adding your country as well. eg:\n`{ctx.prefix}weather <city name>,<country name>`")
    
    @commands.command(help="Shows you info about a Pokémon", aliases=['pokemon', 'poke', 'pokémon', 'pokédex'])
    async def pokedex(self, ctx, pokemon):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://some-random-api.ml/pokedex?pokemon={pokemon.lower()}") as r:
                    res = await r.json()
                if r.status != 200:
                    return await ctx.send("Error!")
                await cs.close()
                embed = discord.Embed(title=f"{res[0]['name'].title()} • #{res[0]['id']}", colour=self.client.colour)
                embed.set_author(name=f'The {" ".join(res[0]["species"])}')
                embed.set_thumbnail(url=res[0]['sprites']['normal'])
                evo_line = []
                for e in res[0]['family']['evolutionLine']:
                    if str(e).lower() == pokemon.lower():
                        evo_line.append(f"**{e}**")
                    else:
                        evo_line.append(e)
                n = '\n'
                embed.description = f" ".join([TYPES[item.lower()] for item in res[0]['type']])
                embed.description += f'\n<:pokeball:715599637079130202> {res[0]["description"]}\n**{res[0]["height"]}**\n**{res[0]["weight"]}**'
                embed.add_field(name='Evolution Line',
                                value=f'{" → ".join(evo_line)}' or "**{0}**".format(str(pokemon).capitalize()),
                                inline=False)
                embed.add_field(name='Abilities', value=', '.join([f'`{i}`' for i in res[0]['abilities']]),
                                inline=False)
                embed.add_field(name='Base Stats',
                                value=f"{f'{n}'.join([f'**{STAT_NAMES[key]}:** `{value}`' for key, value in res[0]['stats'].items()])}",
                                inline=False)
                await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, error, Pokémon not found!")
    
    @commands.command(help="Urban Dictionary", aliases=['urban', 'define', 'def'])
    @commands.is_nsfw()
    async def urbandict(self, ctx, *, terms):
        try:
            embeds = []
            async with aiohttp.ClientSession() as cs:
                async with cs.get('http://api.urbandictionary.com/v0/define', params={'term': terms}) as r:
                    res = await r.json()
                await cs.close()
                for item in res['list']:
                    embed = discord.Embed(color=self.client.colour)
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
            menu.add_info_fields({"<:author:734991429843157042>": "The author of the post",
                                  ":thumbsup:": "How many thumbs up the post has",
                                  ":thumbsdown:": "How many thumbs down the post has"})
            await menu.start(ctx)
        except Exception as error:
            await ctx.send(error.__class__.__name__)
            await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, term not found on urban dictionary.")
    
    @commands.command()
    async def fact(self, ctx):
        """Random fact"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://useless-facts.sameerkumar.website/api") as r:
                res = await r.json()
                await cs.close()
        await ctx.send(embed=discord.Embed(title=res['data'], colour=self.client.colour))
    
    @commands.command()
    async def pypi(self, ctx, *, package):
        """Shows info on a PyPi package"""
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://pypi.org/pypi/{package}/json") as r:
                    res = await r.json()
                await cs.close()
        except Exception as er:
            if isinstance(er, aiohttp.ContentTypeError):
                return await ctx.send(
                    f"<:warning:727013811571261540> **{ctx.author.name}**, package not found! Check for spelling.")
            else:
                return await ctx.send(f"Unknown error occured: {er.__class__.__name__}. Code: {r.status}")
        
        embed = discord.Embed(colour=self.client.colour)
        char = '\u200b' if not res['info']['author_email'] else f' • {res["info"]["author_email"]}'
        embed.title = f"<:pypi:740694184763064393>  `pip install {res['info']['name']}=={res['info']['version']}`"
        embed.description = f"{res['info']['summary']}\n"
        if res['info']['requires_python']:
            versions = res['info']['requires_python'].replace("*", "").split(",")
        else:
            versions = ['???']
        embed.description += f"<:author:734991429843157042> **{res['info']['author']}{char}**\n<:python:706850228652998667> {' | '.join([f'**{version}**' for version in versions])}\n<:license:737733205645590639> **{res['info']['license'] or '???'}**\n<:releases:734994325020213248> **{len(res['releases'])}**"
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
            resp = await self.bot.ask(text, ctx.author.id)
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
        embed = discord.Embed(colour=self.client.colour,
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
        embed = discord.Embed(colour=self.client.colour,
                              description=f"**{from_lang.capitalize()}**\n{message}\n\n**{to_lang.capitalize()}**\n{res.text}\n\n**Pronunciation**\n{res.pronunciation}").set_author(
            name='Translated Text',
            icon_url="https://cdn3.iconfinder.com/data/icons/google-suits-1/32/18_google_translate_text_language_translation-512.png")
        return await ctx.send(embed=embed.set_footer(text=f"{res.confidence * 100}% confident"))
    
    @commands.command(aliases=['wiki'])
    async def wikipedia(self, ctx, *, terms):
        try:
            async with ctx.typing():
                wiki = aiowiki.Wiki.wikipedia("en")
                res = await wiki.opensearch(terms)
                tts = []
                embeds = []
                for i in res:
                    tts.append(i.title)
                for page in tts:
                    p = wiki.get_page(page)
                    embed = discord.Embed(colour=self.client.colour,
                                          description=(__import__('html').unescape(await p.summary()))[:1000] + "...",
                                          title=page)
                    embed.url = f"https://en.wikipedia.org/wiki/{str(page).replace(' ', '_')}"
                    embeds.append(embed)
                source = paginator.EmbedSource(embeds)
            await wiki.close()
            await paginator.CatchAllMenu(source=source).start(ctx)
        except IndexError:
            await ctx.send("Not found.")
    
    @commands.command(aliases=['af'])
    async def animalfact(self, ctx, animal=None):
        """Shows a fact about an animal of your choice."""
        animals = ['dog', 'cat', 'panda', 'fox', 'bird', 'koala']
        if not animal:
            return await ctx.send(f"Valid Animal Choices:\n" + "\n".join([f"• {x}" for x in animals]))
        if animal.lower() not in animals:
            return await ctx.send(f"That is not a valid animal! Valid animals include {', '.join(animals)}.")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://some-random-api.ml/facts/{animal.lower()}') as t:
                resp = await t.json()
            await cs.close()
            return await ctx.send(f"Random **{animal.capitalize()}** Fact:" + "\n" + resp['fact'])
    
    # https://some-random-api.ml/img/cat
    
    @commands.command(aliases=['aimg'])
    async def animalimg(self, ctx, *, animal=None):
        """Shows an image of an animal of your choice."""
        animals = ['dog', 'cat', 'panda', 'fox', 'birb', 'koala', 'fox', 'red panda']
        if not animal:
            return await ctx.send(f"Valid Animal Choices:\n" + "\n".join([f"• {x}" for x in animals]))
        if animal.lower() not in animals:
            return await ctx.send(f"That is not a valid animal! Valid animals include {', '.join(animals)}.")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://some-random-api.ml/img/{animal.lower().replace(" ", "_")}') as t:
                resp = await t.json()
            await cs.close()
            return await ctx.send(
                embed=discord.Embed(description=f"Cute {animal.title()}!", colour=self.client.colour).set_image(
                    url=resp['link']))
    
    @commands.command(aliases=['g'])
    async def google(self, ctx, *, query=None):
        """Shows you google search results for a specified query"""
        client = async_cse.Search(token['google_key'])
        results = await client.search(query, safesearch=not(ctx.channel.is_nsfw()))
        embeds = []
        for res in results:
            embeds.append(
                discord.Embed(colour=self.client.colour, title=res.title, description=res.description, url=res.url))
        source = paginator.EmbedSource(embeds)
        await client.close()
        await paginator.CatchAllMenu(source=source).start(ctx)
    
    @commands.command()
    async def rtfs(self, ctx, *, query: str = None):
        """Shows results from the discord.py sourcecode"""
        if not query:
            return await ctx.send("https://discordpy.readthedocs.io/en/latest/")
        if query.startswith("discord."):
            query = query[8:]
        elif query.startswith("commands."):
            query = query[9:]
        else:
            query = query
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://rtfs.eviee.me/dpy?search={query}") as r:
                res = await r.json()
            if not res:
                return await ctx.send("no results.")
        await cs.close()
        embed = discord.Embed(color=self.client.colour)
        data = await fetch_rtfs(res)
        source = paginator.IndexedListSource(data, embed=embed, per_page=5, show_index=False)
        await paginator.CatchAllMenu(source=source).start(ctx)

    @commands.command(aliases=['gif'])
    @commands.is_nsfw()
    async def giphy(self, ctx, *, query):
        """Get a random gif based on your query"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://api.giphy.com/v1/gifs/search?q=' + query + f'&api_key={token["giphy"]}&limit=10') as r:
                res = await r.json()
        data = res.get('data')
        embeds = []
        for item in data:
            embed = discord.Embed(colour=self.client.colour, title=f"> {item.get('title')}")
            embed.set_thumbnail(url='https://image.ibb.co/b0Gkwo/Poweredby_640px_Black_Vert_Text.png')
            embed.set_image(url=item.get('images')['original']['url'])
            embeds.append(embed)
        source = paginator.EmbedSource(embeds)
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)
#

def setup(client):
    client.add_cog(Api(client))
