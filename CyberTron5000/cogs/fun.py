import json
import random
import string
from asyncio import TimeoutError
from datetime import datetime as dt
from io import BytesIO
from time import time

import discord
from discord.ext import commands, flags
from PyDictionary import PyDictionary as dictionary
from humanize import naturaltime as nt
from jikanpy import AioJikan
from sr_api import Client

from CyberTron5000.utils import (
    paginator,
    cyberformat
)
from CyberTron5000.utils.lists import (
    INDICATOR_LETTERS,
    ANIMALS,
    EMOTIONS
)


class Fun(commands.Cog):
    """Fun commands"""

    def __init__(self, bot):
        self.bot = bot
        self.sr = Client()
        self._dictionary = dictionary()

    @commands.command()
    async def horror(self, ctx, limit: int = 5):
        """spoopy"""
        posts = []
        async with self.bot.session.get(f"https://www.reddit.com/r/twosentencehorror/hot.json") as r:
            res = await r.json()
            for i in res['data']['children']:
                posts.append(i['data'])
            counter = 0
            embeds = []
            async with ctx.typing():
                for s in random.sample(posts, len(posts)):
                    text = cyberformat.shorten(f"{s['title']}\n{s['selftext']}")
                    embeds.append(discord.Embed(description=text[:2000], colour=self.bot.colour))
                    counter += 1
                    if counter == limit:
                        break
                    else:
                        continue
        p = paginator.CatchAllMenu(paginator.EmbedSource(embeds))
        await p.start(ctx)

    @commands.command()
    async def pfpcycle(self, ctx):
        """if you're reading this it probably isnt your business"""
        pfps = ['http://tinyurl.com/y8ccnxm3',
                'https://images-ext-1.discordapp.net/external/6HjseNKji1C5wbK9Wb_jnIluzFWrCRW6xqhfboNtDDI/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/350349365937700864/bbbff13a570231108b7afa383416b62a.png',
                'http://tinyurl.com/ycjuvusq',
                'https://cdn.discordapp.com/avatars/350349365937700864/f38bc11cf4360a9267a55962fcd71809.png?size=1024',
                'https://media.discordapp.net/attachments/381963689470984203/732283634190516304/coolweavile.png?width=962&height=962',
                'https://images-ext-1.discordapp.net/external/XVtT9nLyPYTWfNw4GSjvRMKibuKafi6_VCyVwSfW4C8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/350349365937700864/d027959b2a204f7587092a7a249e7377.png?width=962&height=962',
                'https://media.discordapp.net/attachments/735325249138065468/735681377785348156/image0.png',
                'https://media.discordapp.net/attachments/735325249138065468/735681378292596736/image1.png',
                'https://media.discordapp.net/attachments/735325249138065468/735681378867478528/image2.png',
                'https://media.discordapp.net/attachments/735325249138065468/735681379387441152/image3.png',
                'https://media.discordapp.net/attachments/735325249138065468/735682125239681074/image0.png'
                'http://i.some-random-api.ml/pokemon/weavile.png']
        embeds = [discord.Embed(colour=self.bot.colour).set_image(url=p) for p in pfps]
        a = paginator.CatchAllMenu(paginator.EmbedSource(embeds))
        await a.start(ctx)

    @commands.group(invoke_without_command=True, help="Replies with what you said and deletes your message.",
                    aliases=['say'])
    async def reply(self, ctx, *, message):
        await ctx.send(message)

    @reply.command(invoke_without_command=True,
                   help="Replies with what you said and deletes your message, but in an embed.")
    async def embed(self, ctx, *, message):
        await ctx.send(embed=discord.Embed(title=message, colour=self.bot.colour))

    @reply.command(invoke_without_command=True,
                   help="Replies with what you said and deletes your message, but in a different channel.")
    async def echo(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(message)
        await ctx.message.add_reaction(emoji=ctx.tick())

    @reply.command(invoke_without_command=True, help="Replies with what you said and deletes your message, but UwU.")
    async def owo(self, ctx, *, message):
        await ctx.send(cyberformat.hyper_replace(text=message, old=['r', 'l', 'R', 'L'], new=['w', 'w', "W", "W"]))

    @reply.command(help="🅱", invoke_without_command=True)
    async def b(self, ctx, *, message):
        await ctx.send(cyberformat.hyper_replace(text=message, old=['b', 'B', 'D', 'd'], new=['🅱', '🅱', "🅱", "🅱"]))

    @reply.command(aliases=['msg'], help="Message a user something. ", invoke_without_command=True)
    async def message(self, ctx, user: discord.Member, *, message):
        person = self.bot.get_user(user.id)
        await person.send(f"{message}\n\n*(Sent by {ctx.message.author})*")
        await ctx.message.add_reaction(emoji=ctx.tick())

    @reply.command(help="Spams a message.", invoke_without_command=True)
    async def spam(self, ctx, *, message):
        await ctx.send(f"{message} " * 15)

    @reply.command(invoke_without_command=True, aliases=['emoji', 'em'])
    async def indicator(self, ctx, *, message):
        """reply in emojis"""
        msg = ''
        letters = list(string.ascii_lowercase)
        for x in message:
            if x in letters:
                msg += f':regional_indicator_{x}:'
            else:
                msg += INDICATOR_LETTERS.get(x, x)
        await ctx.send('\u200b' + msg)

    @reply.command()
    async def mock(self, ctx, *, message):
        """Like that spongebob meme"""
        await ctx.send(cyberformat.better_random_char(message))

    @commands.command(help="Asks the mystical Ouija Board a question...")
    async def askouija(self, ctx, *, question):
        ouija_responses = [
            'Help',
            'Bruh',
            'dumb',
            'You dumb',
            'Hey gamers'
            'Infinity',
            'God damn ur ugly',
            'Gamers',
            'Gamers Unite',
            'Fricken amateur',
            'Fricken doofus',
            'Yo',
            'Joe mama',
            'No',
            'yes',
            'perhaps',
            'Waluigi',
            'Bruh Moment',
            'Moment of the Bruh',
            'Puh-leaze',
            'Vibe Check']
        ouija_choice = random.choice(ouija_responses)
        ouija_says = str("You asked me... '_{}_'... I respond... {}".format(question, ouija_choice))
        await ctx.send(ouija_says)

    @commands.command(aliases=['cf'], help="Flips a coin.")
    async def coinflip(self, ctx, *, clause: str = None):
        tails = discord.Embed(title="Tails!", colour=self.bot.colour).set_image(
            url='https://upload.wikimedia.org/wikipedia/en/thumb/3/37/Quarter_Reverse_2010.png/220px-Quarter_Reverse_2010.png')
        heads = discord.Embed(title="Heads!", colour=self.bot.colour).set_image(
            url='https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Quarter_Obverse_2010.png/220px-Quarter_Obverse_2010.png')
        embed = random.choice([heads, tails])
        embed.set_author(name=clause, icon_url=ctx.author.avatar_url) if clause else None
        await ctx.send(embed=embed)

    @commands.command(help="How bigbrain are you? Find out.")
    async def iq(self, ctx, *, member: discord.Member = None):
        member = member or ctx.message.author
        embed = discord.Embed(
            colour=self.bot.colour, title='IQ Rating Machine <:bigbrain:703735142509969408>',
            timestamp=ctx.message.created_at
        )
        embed.set_author(name="{}".format(member.display_name), icon_url=member.avatar_url)
        embed.add_field(name="What is your IQ?",
                        value=f"{member.display_name} has an IQ of {random.randint(1, 101)}.")
        await ctx.send(embed=embed)

    @commands.command(help="Fite")
    async def fight(self, ctx, opponent: discord.Member, *, weapon):
        author = ctx.message.author
        if opponent == author:
            await ctx.send("You can't fight yourself. Snap out of it. The accident was three years ago.")
        else:
            enemy_weapon = random.choice([
                " Sword of Mega Doom",
                " Epic Gun",
                " Mega Epic Gun",
                " Grenade",
                " Amazing Bruh Machine",
                " Gun Lmao",
                " Hyper Epic Gun",
                " 'Not even trying at this point' Rifle",
                " Grand Sword of Chaos",
                " Excalibur",
                " Master Sword",
                " Storm Pegasus",
                " Rock Leone",
                " Lightning L-Drago"
            ])
            run = random.choice([
                " but they miraculously fight back with their fists and beat you to the ground! You Lose!",
                " and they get scared and flee! You Win!"
            ])
            possibilities = random.choice([
                " but they escape! You lose!",
                " and they get rekt, m8. You win!",
                " and they get blasted into the Shadow Realm! You win!",
                " but they retaliate with their**{}**! You knock it out of their hands,{}".format(enemy_weapon, run),
                " but they fight back with their**{}**! They use it to knock your **{}** "
                "out of your hands, and finish you off with their**{}**! You Lose!".format(
                    enemy_weapon, weapon, enemy_weapon),
                " but they fight back with their**{}**! You two have a hard clash, but you end up losing! You Lose!".format(
                    enemy_weapon),
                " but they fight back with their**{}**! You two have a hard clash, and you end up winning! You Win!".format(
                    enemy_weapon),
                " and you pounce at them, but activate their trap card,**{}**. Chances "
                "look slim for you, but... they end up destroying your **{}** and win. You Lose!".format(
                    enemy_weapon, weapon),
                " and you pounce at them, but activate their trap card,**{}**. Chances "
                "look slim for you, but... in the nick of time, you end up Yeeting them with your **{}**! You Win!".format(
                    enemy_weapon, weapon),
                " and they drop their**{}**! You pick it up and use both the **{}** and**{}** to "
                "yeet them! You Win!".format(
                    enemy_weapon, weapon, enemy_weapon),
                " and they drop their**{}**! You pick it up and use both the **{}** and**{}**, "
                "but they sneak up from behind and steal your own **{}**. You two have a hard "
                "fight, but they best you! You Lose!".format(
                    enemy_weapon, weapon, enemy_weapon, weapon),
                " and they drop their**{}**! You pick it up and use both the **{}** and**{}**, "
                "but they sneak up from behind and steal both weapons! Things are looking bleak "
                "for you, so you engage in a fist fight with them, and after a few minutes, "
                "you're both found lying on the floor. It's a draw!".format(
                    enemy_weapon, weapon, enemy_weapon),
                " and trigger their PTSD. You Win!",
                " but you guys decide to make peace. It's a draw!"
            ])
            embed = discord.Embed(
                colour=self.bot.colour, title='Fight Results! :crossed_swords:', timestamp=ctx.message.created_at
            )

            embed.set_author(name="{} vs {}".format(author.display_name, opponent.display_name),
                             icon_url=author.avatar_url)
            embed.add_field(name="_Who Won?_",
                            value="You fight **{}** with **{}**,{}".format(opponent.display_name, weapon,
                                                                           possibilities))
            await ctx.send(embed=embed)

    @commands.command(help="Ask the Bot about your peers")
    async def who(self, ctx, *, question=None):
        member = random.choice(ctx.guild.members)
        embed = discord.Embed(
            colour=self.bot.colour,
            title=f"Answer: {member.display_name}",
        )
        question = question or "?"
        embed.set_author(name="Who " + question)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, aliases=["em"],
                    help="do an emoji from a different server that cybertron is in.")
    async def emoji(self, ctx, *emoji: discord.Emoji):
        a = []
        for item in emoji:
            a.append(self.bot.get_emoji(item.id))
        await ctx.send("".join([str(a) for a in a]))

    @emoji.command()
    async def url(self, ctx, *emoji: discord.Emoji):
        a = []
        for item in emoji:
            a.append(self.bot.get_emoji(item.id))
        await ctx.send(" ".join([str(a.url) for a in a]))

    @commands.command(aliases=['gt'])
    async def greentext(self, ctx):
        """Write a greentext story"""
        story = []
        await ctx.send(
            f"Greentext story starting! Type `{ctx.prefix}quit`, `{ctx.prefix}exit`, or `{ctx.prefix}finish` to see your final story!")
        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=300, check=lambda x: x.author == ctx.author)
                if msg.content in (f'{ctx.prefix}quit', f'{ctx.prefix}exit', f'{ctx.prefix}finish'):
                    break
                story.append(msg.content.replace('```', '\u200b'))
                await msg.add_reaction(ctx.tick())
            except TimeoutError:
                break
        story = '\n'.join([f'>{line}' for line in story])
        return await ctx.send(embed=discord.Embed(colour=discord.Color.green(),
                                                  description=f"**{ctx.author}**'s story```css\n{story}\n```"))

    @commands.command(aliases=['bin'])
    async def binary(self, ctx, *, message):
        """Convert text to binary."""
        binary = await self.sr.encode_binary(message)
        await ctx.send(f"```py\n{binary}```")

    @commands.command(aliases=['fb', 'from-bin'])
    async def from_binary(self, ctx, *, binary):
        """Convert text from binary."""
        binary = await self.sr.decode_binary(binary)
        await ctx.send(binary)

    @commands.command()
    async def owner(self, ctx):
        """Shows you who made this bot"""
        return await ctx.send(f"it is {self.bot.owner}")

    @commands.command()
    async def anime(self, ctx, *, query):
        async with AioJikan() as a:
            naruto = await a.search(search_type='anime', query=query)
        res = naruto['results'][0]
        o = []
        embed = discord.Embed(color=self.bot.colour)
        embed.set_thumbnail(url=res['image_url'])
        embed.title = f"{res['title']}"
        embed.url = f"{res['url']}"
        embed.description = f"{naruto['results'][0]['synopsis']}"
        embed.add_field(name="Info",
                        value=f"Type | **{res['type']}**\n📺 | **{res['episodes']}**\n:star:️ | **{res['score']}**\n<:member:731190477927219231> | **{res['members']:,}**")
        for x in range(2, len(naruto['results'])):
            o.append(f"**{naruto['results'][x]['title']}**")
        embed.add_field(name="Other Entries", value=f"\n".join(o[:5]))
        await ctx.send(embed=embed)

    @commands.command(aliases=['choice'])
    async def chose(self, ctx, *choices):
        await ctx.send(random.choice(choices))

    async def get_all_todo(self, id: int = None):
        if not id:
            return await self.bot.db.fetch("SELECT * FROM todo")
        else:
            return await self.bot.db.fetch("SELECT * FROM todo WHERE user_id = $1", id)

    @commands.group(invoke_without_command=True)
    async def todo(self, ctx):
        """Shows your current todo list"""
        items = []
        results = sorted((await self.get_all_todo(ctx.author.id)), key=lambda x: x['time'])
        for each in results:
            time = dt.utcfromtimestamp(each['time'])
            since = nt(dt.utcnow() - time)
            if each['description']:
                desc_em = "❔"
            else:
                desc_em = ""
            items.append(f"[{each['todo']}]({each['message_url']}) (ID: {each['id']} | Created {since}) {desc_em}")
        source = paginator.IndexedListSource(data=items, embed=discord.Embed(colour=self.bot.colour),
                                             title="Items (`❔` indicates that the todo has a description)", per_page=5)
        menu = paginator.CatchAllMenu(source=source)
        menu.add_info_fields({"❔": "Indicates that the todo has a description"})
        await menu.start(ctx)

    @todo.command()
    async def add(self, ctx, *, todo):
        """Adds an item to your todo list"""
        if len(todo) > 50:
            return await ctx.send("Your todo is too long. Please be more consice.")
        id = random.randint(1, 99999)
        await self.bot.db.execute(
            "INSERT INTO todo (todo, id, time, message_url, user_id) VALUES ($1, $2, $3, $4, $5)", todo, id, time(),
            str(ctx.message.jump_url), ctx.author.id)
        await ctx.send(f"{ctx.tick()} Inserted `{todo}` into your todo list! (ID: `{id}`)")

    @todo.command(aliases=['rm', 'remove'])
    async def resolve(self, ctx, *id: int):
        """Resolves an item from your todo list"""
        items = await self.get_all_todo(ctx.author.id)
        todos = [item[0] for item in items]
        ids = [item[1] for item in items]
        if any(item not in ids for item in id):
            return await ctx.send("You passed in invalid id's!")
        message = []
        for i in id:
            message.append(f"• {todos[ids.index(i)]}")
            await self.bot.db.execute("DELETE FROM todo WHERE user_id = $1 AND id = $2", ctx.author.id, i)
        await ctx.send(
            f"{ctx.tick()} Deleted **{len(id)}** items from your todo list:\n" + "\n".join(message))

    @todo.command()
    async def list(self, ctx):
        """Shows your todo list"""
        command = self.bot.get_command('todo')
        await ctx.invoke(command)

    @todo.command()
    async def clear(self, ctx):
        """Clears all of your todos"""
        num = len((await self.bot.db.fetch("SELECT * FROM todo WHERE user_id = $1", ctx.author.id)))
        await self.bot.db.execute("DELETE FROM todo WHERE user_id = $1", ctx.author.id)
        await ctx.send(f"{ctx.tick()} Deleted **{num}** items from your todo list!")

    @todo.command(aliases=['show'])
    async def info(self, ctx, id: int):
        """Shows you info on a todo"""
        results = await self.bot.db.fetch("SELECT * FROM todo WHERE id = $1", id)
        if not results:
            raise commands.BadArgument(f'{id} is not a valid todo!')
        results = results[0]
        embed = discord.Embed(colour=self.bot.colour)
        embed.title = f"{results['todo']} » `{results['id']}`"
        time = dt.utcfromtimestamp(results['time'])
        since = nt(dt.utcnow() - time)
        embed.description = f'{results["description"] or ""}\n'
        embed.description += f"<:clock:738186842343735387> **{since}**\n"
        embed.description += f"**{time.strftime('%A %B %d, %Y at %I:%M %p')}**"
        await ctx.send(embed=embed)

    @todo.command(aliases=['add_desc', 'ad'])
    async def describe(self, ctx, id: int, *, description):
        """Add a description for your todo"""
        results = await self.bot.db.fetch("SELECT * FROM todo WHERE id = $1", id)
        if not results:
            raise commands.BadArgument(f'{id} is not a valid todo!')
        if len(description) > 250:
            return await ctx.send("That description is too long!")
        await self.bot.db.execute("UPDATE todo SET description = $1 WHERE id = $2", description, id)
        await ctx.send(
            f"{ctx.tick()} Set todo description for `{id}` ({results[0]['todo']}) to `{description}`")

    @flags.add_flag("--limit", type=int, default=500)
    @flags.add_flag("--channel", type=discord.TextChannel)
    @flags.command()
    async def snipe(self, ctx, **flags):
        """Shows the most recently deleted messages in a given channel"""
        # i know i shouldnt be using json for this
        channel = flags.get('channel') or ctx.channel
        with open('./json_files/snipes.json', 'r') as f:
            snipes = json.load(f)
        try:
            channel_snipes = snipes[str(channel.id)]
        except KeyError:
            return await ctx.send(f"{channel} has no deleted messages.")
        embeds = []
        for snipe in reversed(channel_snipes[:flags.get('limit')]):
            author = self.bot.get_user(int(snipe['author'])) or await self.bot.fetch_user(int(snipe['author']))
            embed = discord.Embed(colour=self.bot.colour)
            desc = snipe['content']
            if not desc and snipe.get('embed'):
                desc = '`<Embedded Message>`'
            embed.description = desc
            since = dt.strptime(snipe['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            embed.set_author(name=f"{author} said in {str(channel)}", icon_url=author.avatar_url)
            embed.timestamp = since
            embeds.append(embed)
        source = paginator.EmbedSource(embeds, footer=False)
        await paginator.CatchAllMenu(source).start(ctx)

    @commands.command(aliases=['af'])
    async def animalfact(self, ctx, animal=None):
        """Shows a fact about an animal of your choice."""
        if not animal:
            return await ctx.send(
                f"**Valid Animal Choices:**\ncat, dog, koala, fox, bird, elephant, panda, racoon, kangaroo, giraffe, whale")
        try:
            animal = str(animal).lower().replace(' ', '_')
            em = ANIMALS.get(animal)
            fact = await self.sr.get_fact(animal)
            await ctx.send(f"{em} **Random {animal.replace('_', ' ').title()} Fact:**\n{fact}")
        except Exception as error:
            return await ctx.send(error)

    async def get_attachement(self, image_url: str, ext='png') -> discord.File:
        """Gives you a valid image attachment of any url"""
        async with self.bot.session.get(image_url) as r:
            data = await r.read()
        image = BytesIO(data)
        return discord.File(image, filename=f'image.{ext}')

    @commands.command(aliases=['aimg'])
    async def animalimg(self, ctx, *, animal=None):
        """Shows an image of an animal of your choice."""
        if not animal:
            return await ctx.send(
                f"**Valid Animal Choices:**\ncat, dog, koala, fox, birb, red panda, panda, racoon, kangaroo")
        try:
            async with ctx.typing():
                animal = str(animal).lower().replace(' ', '_')
                image = await self.sr.get_image(animal)
                file = await self.get_attachement(image.url)
                await ctx.send(f"{ANIMALS.get(animal, '')} **Random {animal.replace('_', ' ').title()} Image:**",
                               file=file)
        except Exception as error:
            return await ctx.send(error)

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        async with ctx.typing():
            image = await self.sr.get_gif('hug')
            file = await self.get_attachement(image.url, 'gif')
        await ctx.send(f"{EMOTIONS['hug']} **{ctx.author.display_name}** hugged **{member.display_name}**!", file=file)

    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        async with ctx.typing():
            image = await self.sr.get_gif('pat')
            file = await self.get_attachement(image.url, 'gif')
        await ctx.send(f"{EMOTIONS['pat']} **{ctx.author.display_name}** patted **{member.display_name}**!", file=file)

    @commands.command()
    async def facepalm(self, ctx):
        async with ctx.typing():
            image = await self.sr.get_gif('face-palm')
            file = await self.get_attachement(image.url, 'gif')
        await ctx.send(f"{EMOTIONS['face-palm']} **{ctx.author.display_name}** facepalmed!", file=file)

    @commands.command()
    async def wink(self, ctx):
        async with ctx.typing():
            image = await self.sr.get_gif('wink')
            file = await self.get_attachement(image.url, 'gif')
        await ctx.send(f"{EMOTIONS['wink']} **{ctx.author.display_name}** winked!", file=file)

    @commands.command()
    async def dog(self, ctx):
        """Shows you an image of a dog."""
        async with self.bot.session.get('https://dog.ceo/api/breeds/image/random') as r, ctx.typing():
            data = await r.json()
        file = await self.get_attachement(data['message'])
        await ctx.send(f"{ANIMALS.get('dog')} **Random Dog Image**", file=file)

    def format_meanings(self, ret: dict) -> str:
        message = ''
        for index, value in ret.items():
            message += f"\n**{index}**\n"
            for num, _def in enumerate(value, 1):
                message += f"[{num}] {_def}\n"
        return message

    @commands.group(aliases=['dictionary'], invoke_without_command=True)
    async def word(self, ctx, *, word):
        """Fetch a word's definition"""
        # thanks to deviljamjar for this idea
        # find the original here: https://github.com/DevilJamJar/DevilBot/blob/master/cogs/utility.py/#L48-#L65
        async with ctx.typing():
            try:
                ret = await self.bot.loop.run_in_executor(None, self._dictionary.meaning, word)
            except Exception as error:
                raise error
            embed = discord.Embed(colour=self.bot.colour, title=word.lower())
            if not ret:
                raise commands.BadArgument("this word was not found in the dictionary!")
            embed.description = self.format_meanings(ret)
        await ctx.send(embed=embed)

    @word.command(aliases=['syn'])
    async def synonyms(self, ctx, *, word):
        """Shows you the synonyms of a word."""
        async with ctx.typing():
            try:
                ret = await self.bot.loop.run_in_executor(None, self._dictionary.synonym, word)
            except Exception as error:
                raise error
            embed = discord.Embed(colour=self.bot.colour, title=word.lower())
            embed.description = ', '.join(ret)
        await ctx.send(embed=embed)

    @word.command(aliases=['ant'])
    async def antonyms(self, ctx, *, word):
        """Shows you the antonyms of a word."""
        async with ctx.typing():
            try:
                ret = await self.bot.loop.run_in_executor(None, self._dictionary.antonym, word)
            except Exception as error:
                raise error
            embed = discord.Embed(colour=self.bot.colour, title=word.lower())
            embed.description = ', '.join(ret)
        await ctx.send(embed=embed)

    @word.command()
    async def many(self, ctx, *words):
        """Get information on many words"""
        command = self.bot.get_command('words')
        await ctx.invoke(command, *words)

    @commands.command()
    async def words(self, ctx, *words):
        """Get information on many words"""
        async with ctx.typing():
            _dict = dictionary(*words)
            try:
                ret = await self.bot.loop.run_in_executor(None, _dict.getMeanings)
            except Exception as error:
                raise error
            embed = discord.Embed(colour=self.bot.colour)
            embed.title = "Words"
            not_found = list()
            for word in words:
                meanings = ret.get(word)
                if not meanings:
                    not_found.append(word)
                    continue
                embed.add_field(name=word.lower(), value=self.format_meanings(meanings))
        if not_found:
            embed.set_footer(text=', '.join(not_found) + " were not found.")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            return await ctx.send("You passed in too many words!")

    @commands.command()
    async def funpy(self, ctx):
        await ctx.send('everyone ~~!!!!~~ hates funpy')

def setup(bot):
    bot.add_cog(Fun(bot))
