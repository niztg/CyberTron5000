import asyncio
import random

import aiotrivia
import discord
from discord.ext import commands
from unidecode import unidecode
from contextlib import suppress
from async_timeout import timeout

from CyberTron5000.utils import cyberformat, lists
from CyberTron5000.utils.models.fighter import Fighter


class Games(commands.Cog):
    """Games!"""

    def __init__(self, bot):
        self.bot = bot
        self.headers = {'token': bot.config.dagpi_token}
        self.trivia = aiotrivia.TriviaClient()

    # rock paper scissors, shoot
    @commands.command(aliases=['rps'], help="Rock paper scissors shoot")
    async def rockpaperscissors(self, ctx):
        rps_dict = {
            "🗿": {
                "🗿": "draw",
                "📄": "lose",
                "✂": "win"
            },
            "📄": {
                "🗿": "win",
                "📄": "draw",
                "✂": "lose"
            },
            "✂": {
                "🗿": "lose",
                "📄": "win",
                "✂": "draw"
            }
        }
        choice = random.choice([*rps_dict.keys()])
        msg = await ctx.send(embed=discord.Embed(colour=self.bot.colour, description=f"**Choose one 👇**").set_footer(
            text=f"You have 15 seconds."))
        for r in rps_dict.keys():
            await msg.add_reaction(r)
        try:
            r, u = await self.bot.wait_for('reaction_add', timeout=15, check=lambda re, us: us == ctx.author and str(
                re) in rps_dict.keys() and re.message.id == msg.id)
            play = rps_dict.get(str(r.emoji))
            await msg.edit(embed=discord.Embed(colour=self.bot.colour,
                                               description=f"Result: **{play[choice].title()}**\nI Played: **{choice}**\nYou Played: **{str(r.emoji)}**"))
        except asyncio.TimeoutError:
            await ctx.send(f"Boo, you ran out of time!")

    # kiss marry kill command

    @commands.command(help="Kiss, marry, kill.", aliases=['kmk'])
    async def kissmarrykill(self, ctx):
        members = random.sample(ctx.guild.members, k=3)
        kmk = {'😘': 'kiss (😘)', '👫': 'marry (👫)', '🔪': 'kill(🔪)'}
        embed = discord.Embed(colour=self.bot.colour)
        for m in members:
            embed.add_field(name=m.display_name, value="\u200b")
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)

        async def _add_reactions(_msg, _reactions):
            for r in _reactions:
                await _msg.add_reaction(r)

        initial_len = len(kmk)
        while len(kmk) > 1:
            index = initial_len - len(kmk)
            ask_kmk = ', '.join(kmk.values())
            embed.description = f"**Would you {ask_kmk} {members[index].display_name}?**"
            msg = await ctx.send(embed=embed)
            self.bot.loop.create_task(_add_reactions(msg, kmk))

            def check(reaction, user):
                return str(reaction.emoji) in kmk and user == ctx.author and reaction.message.id == msg.id

            try:
                reaction, user = await self.bot.wait_for(
                    'reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Didn't respond in time")
            embed.set_field_at(index, name=members[index].display_name, value=str(reaction.emoji))
            kmk.pop(str(reaction.emoji))

        if len(kmk) != 1:
            print('error')
        embed.description = '**Results**'
        index = initial_len - len(kmk)
        embed.set_field_at(index, name=members[index].display_name, value=kmk.popitem()[0])
        await ctx.send(embed=embed)

    @commands.group(aliases=['wtp'], invoke_without_command=True)
    async def whosthatpokemon(self, ctx):
        """
        Who's that pokemon!?
        """
        async with self.bot.session.get('https://dagpi.tk/api/wtp', headers=self.headers) as r, ctx.typing():
            who = await r.json()
            __name = unidecode(str(who['pokemon']['name'])).lower()
            async with self.bot.session.get(f"https://some-random-api.ml/pokedex?pokemon={__name}") as r2:
                pokemon = await r2.json()
            initial_embed = discord.Embed(colour=self.bot.colour)
            initial_embed.title = "Who's that Pokemon?"
            initial_embed.description = f"Do `{ctx.prefix}hint` for a hint or `{ctx.prefix}cancel` to cancel."
            initial_embed.set_image(url=who.get('question_image'))
            initial_embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)
            answer_embed = discord.Embed(colour=self.bot.colour, title=f"It's {who['pokemon']['name']}!")
            answer_embed.set_image(url=who.get('answer_image'))
        if __name.replace('.', '') == "mrmime":
            await ctx.invoke(ctx.command)
            return
        msg = await ctx.send(embed=initial_embed)
        content = "<:pokeball:715599637079130202> Attempts: **{0}/3**"
        hints = [
            f"**Evolution Line**\n{' → '.join([unidecode(p).lower().capitalize() for p in pokemon['family']['evolutionLine']])}".replace(
                __name.capitalize(), "???"),
            f"**Pokédex Entry**\n{unidecode(pokemon['description']).lower().replace(__name, '???').capitalize()}",
            f"`{cyberformat.better_random_char(__name, '_')}`",
            f"**Species**\n{' '.join(pokemon['species'])}",
            f"**Height/Weight**\n{pokemon['height']}/{pokemon['weight']}",
            f"**Generation**\n{pokemon['generation']}"
        ]
        num_hints = 0
        try:
            for attempt in range(3):
                await msg.edit(content=content.format(attempt + 1))
                message = await self.bot.wait_for('message', timeout=30, check=lambda m: m.author == ctx.author)
                __message = unidecode(str(message.content.lower()))
                if __message == __name:
                    answer_embed.description = f"You guessed correctly with **{attempt + 1}** guesses and **{num_hints}** hints!"
                    return await msg.edit(embed=answer_embed, content='')
                elif __message == f"{ctx.prefix}hint":
                    num_hints += 1
                    hint = random.choice(hints)
                    hints.remove(hint)
                    embed = discord.Embed(colour=self.bot.colour)
                    embed.set_author(name=f"Hint",
                                     icon_url="https://cdn.discordapp.com/emojis/715599637079130202.png?v=1")
                    embed.description = hint
                    await ctx.send(embed=embed)
                elif __message == f"{ctx.prefix}cancel":
                    await msg.edit(embed=answer_embed, content='')
                else:
                    continue
            answer_embed.description = "You used up all of your guesses!"
            await msg.edit(embed=answer_embed, content='')
        except asyncio.TimeoutError:
            answer_embed.description = "You ran out of time!"
            await msg.edit(embed=answer_embed, content='')

    @commands.command(help="Get's you a trivia question.", aliases=['tr', 't'])
    async def trivia(self, ctx, difficulty: str = None):
        difficulty = difficulty or random.choice(['easy', 'medium', 'hard'])
        try:
            question = await self.trivia.get_random_question(difficulty)
        except aiotrivia.AiotriviaException:
            return await ctx.send(f'**{difficulty}** is not a valid difficulty!')
        embed = discord.Embed(colour=ctx.bot.colour)
        embed.title = question.question
        responses = question.responses
        random.shuffle(responses)
        embed.description = "\n".join(
            [f':regional_indicator_{lists.NUMBER_ALPHABET[i].lower()}: **{v}**' for i, v in enumerate(responses, 1)])
        embed.add_field(name="Info",
                        value=f'Difficulty: **{question.difficulty.title()}**\nCategory: **{question.category}**')
        embed.set_footer(text="React with the correct answer! | You have 15 seconds")
        emojis = [cyberformat.to_emoji(x) for x in range(len(responses))]
        index = responses.index(question.answer)
        msg = await ctx.send(embed=embed)
        for e in emojis:
            await msg.add_reaction(e)

        def check(reaction: discord.Reaction, user: discord.User):
            return reaction.message.id == msg.id and user.id == ctx.author.id and str(reaction.emoji) in emojis

        correct = emojis[index]

        try:
            r, u = await self.bot.wait_for('reaction_add', check=check, timeout=15)
            if str(r.emoji) == correct:
                await msg.edit(embed=discord.Embed(colour=self.bot.colour,
                                                   description=f"{ctx.tick()} Correct! The answer was {correct}, **{question.answer}**"))
            else:
                await msg.edit(embed=discord.Embed(colour=self.bot.colour,
                                                   description=f"{ctx.tick(False)} Incorrect! The correct answer was {correct}, **{question.answer}**"))
        except asyncio.TimeoutError:
            await msg.edit(embed=discord.Embed(colour=self.bot.colour,
                                               description=f"{ctx.tick(False)} You ran out of time! The correct answer was {correct}, **{question.answer}**"))

    @commands.group(aliases=['gl', 'gtl'], invoke_without_command=True)
    async def guesslogo(self, ctx):
        """
        Guess a random logo!
        """

    @commands.command(aliases=['mm'])
    async def mastermind(self, ctx):
        """Guess a random 4 digit code!"""
        await ctx.send(
            f'**Guess a random 4 digit code!**\nKey:\n{ctx.tick()} - Right number in the right spot.\n<:ticknull:732660186057015317> - Right number in the wrong spot.\n{ctx.tick(False)} - This number does not appear in the code.')
        code = random.sample(list(map(str, list(range(9)))), 4)
        tries = 0
        statuses = {
            0: ctx.tick(False),
            1: "<:ticknull:732660186057015317>",
            2: ctx.tick(True)
        }

        def perfect(responses: list):
            return responses == [2, 2, 2, 2]

        while True:
            final = []
            msg = await self.bot.wait_for(
                'message',
                check=lambda m: (m.author, m.channel) == (ctx.author, ctx.channel)
            )
            msg = msg.content
            if msg == "stop":
                return await ctx.send("Stopping. the code was {}".format("".join(code)))
            if not msg.isdigit() or not len(msg) == 4:
                await ctx.send("{} is not a valid code. Codes are all 4 integers long.".format(msg))
                continue
            data = list(msg)
            multiple = any(data.count(x) > 1 for x in data)
            tries += 1
            for x in range(4):
                if data[x] == code[x]:
                    final.append(2)
                elif data[x] in code:
                    final.append(1)
                elif data[x] not in code:
                    final.append(0)
            if perfect(final):
                return await ctx.send("You won in {} tries! The code was {}".format(tries, "".join(code)))
            else:
                await ctx.send(" ".join(list(map(statuses.get, final))))
                await ctx.send("{} tries".format(tries))
                if multiple:
                    await ctx.send("Note: codes do not contain 2 or more of the same number")

    @commands.command()
    async def fight(self, ctx, member: discord.Member):
        """Fight against anyone!"""
        user_1 = Fighter(ctx.author)
        await ctx.send(f"{member.mention}, {ctx.author} has challenged you to a fight. Do you accept?")
        try:
            msg = await self.bot.wait_for(
                'message',
                timeout=30,
                check=lambda x: x.author == member
            )
            if msg.content.lower().startswith('y'):
                user_2 = Fighter(member)
            else:
                return
        except asyncio.TimeoutError:
            return await ctx.send('out of time')

        prompt = True
        while (not user_1.dead) and (not user_2.dead):
            embed = discord.Embed(description=f"{user_1}\n{user_2}", title="Score", colour=self.bot.colour)
            await ctx.send(embed=embed)
            if prompt:
                user = user_1
                anti_user = user_2
            else:
                user = user_2
                anti_user = user_1

            prompt = not prompt

            await ctx.send(f"{user.name}, `{ctx.prefix}play attack`/`{ctx.prefix}play heal`/`{ctx.prefix}play end`")
            choice = await self.bot.wait_for(
                'message',
                check=lambda x: x.author == user.self and x.content.startswith(f"{ctx.prefix}play")
            )
            choice = choice.content.lower()[len(f"{ctx.prefix}play"):].strip()
            if choice.startswith("a"):
                dmg = random.randint(1, 100)
                dealt = anti_user.update_heath(-dmg)
                await ctx.send(
                    f"{user.name}, you dealt {-dealt} damage with the {random.choice(lists.WEAPONS).strip()}")
                if anti_user.dead:
                    embed2 = discord.Embed(description=f"{user_1}\n{user_2}", title="Score", colour=self.bot.colour)
                    await ctx.send(embed=embed2)
                    return await ctx.send(f"{user.self.mention}, you win!")
                else:
                    continue
            elif choice.startswith("h"):
                try:
                    heal = user.heal()
                    await ctx.send(f"{user.name}, you healed **{heal}** health!")
                except Exception as error:
                    await ctx.send(error)
                    continue
            elif choice.startswith("e"):
                await ctx.send(embed=embed)
                return await ctx.send(f"{anti_user.self.mention}, you win!")
            else:
                await ctx.send("aint valid.")

    @commands.command(aliases=['ql'])
    async def quiplash(self, ctx):
        """Play Quiplash, the famous Jackbox game!"""
        content = f'➣ **{ctx.author.display_name}**'
        embed = discord.Embed(title=f"Quiplash!",
                              description=f"Type `{ctx.prefix}join` to join. The game will start in "
                                          "60 seconds or with 8 players!", colour=self.bot.colour)
        embed.add_field(name="Players (1)", value=content)
        msg = await ctx.send(embed=embed)
        users = [ctx.author]
        with suppress(asyncio.TimeoutError):
            try:
                async with timeout(60):
                    while True:
                        app = await self.bot.wait_for('message', check=lambda
                            x: x.channel == ctx.channel and x.author not in users and not x.author.bot and x.content == f"{ctx.prefix}join")
                        content += f"\n➣ **{app.author.display_name}**"
                        users.append(app.author)
                        embed.set_field_at(index=0, name=f"Players {len(users)}", value=content)
                        await msg.edit(embed=embed)
                        if len(users) == 8:
                            break
                        continue
            finally:
                await ctx.send("The game is starting!" + "\n" + f"{' '.join([u.mention for u in users])}")
        quip = random.choice(lists.QUIPS)
        for user in users:
            await user.send('This round\'s prompt is: {}'.format(quip))
        finals = []
        answerers = []
        with suppress(asyncio.TimeoutError):
            try:
                while True:
                    async with timeout(60):
                        msg = await self.bot.wait_for('message', check=lambda x: isinstance(x.channel,
                                                                                            discord.DMChannel) and x.author not in answerers and x.author in users)
                        finals.append(msg.content)
                        answerers.append(msg.author)
                        await msg.author.send("Quip noted.")
                        if len(finals) == len(users):
                            break
                        continue
            finally:
                await ctx.send("READY!\n" + f"{' '.join([u.mention for u in users])}")
        if not finals:
            return await ctx.send('no quips :(')
        await ctx.send(f"The Prompt: **{quip}**\nQuips:\n" + "\n".join([f"{i}. {v}" for i, v in enumerate(finals, 1)]))
        await ctx.send("Enter the number of your favourite quip.")
        vote = {}
        for number in range(1, len(finals) + 1):
            vote[str(number)] = 0
        a = 0
        with suppress(asyncio.TimeoutError):
            while True:
                async with timeout(60):
                    msg = await self.bot.wait_for('message', check=lambda
                        x: x.content.isdigit() and x.content in vote.keys() and x.author in users and x.channel == ctx.channel)
                    vote[msg.content] += 1
                    a += 1
                    if a == len(users):
                        break
                    continue
        winner = max(vote.items(), key=lambda m: m[1])
        quip = finals[int(winner[0]) - 1]
        user = answerers[int(winner[0]) - 1]
        await ctx.send(f"Option {winner[0]} is the winner!\n`{quip}`\nwritten by {user}")


def setup(bot):
    bot.add_cog(Games(bot))
