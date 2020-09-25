import asyncio
import random

import aiotrivia
import discord
from discord.ext import commands
from unidecode import unidecode

from CyberTron5000.utils import cyberformat, lists
from CyberTron5000.utils.models.pokemon import Pokemon


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
            f"**Evolution Line**\n{' → '.join([unidecode(p).lower().capitalize() for p in pokemon['family']['evolutionLine']])}".replace(__name.capitalize(), "???"),
            f"**Pokédex Entry**\n{unidecode(pokemon['description']).lower().replace(__name, '???').capitalize()}",
            f"`{cyberformat.better_random_char(__name, '_')}`",
            f"**Species**\n{' '.join(pokemon['species'])}",
            f"**Height/Weight**\n{pokemon['height']}/{pokemon['weight']}",
            f"**Generation**\n{pokemon['generation']}"
        ]
        num_hints = 0
        try:
            for attempt in range(3):
                await msg.edit(content=content.format(attempt+1))
                message = await self.bot.wait_for('message', timeout=30, check=lambda m: m.author == ctx.author)
                __message = unidecode(str(message.content.lower()))
                if __message == __name:
                    answer_embed.description = f"You guessed correctly with **{attempt+1}** guesses and **{num_hints}** hints!"
                    return await msg.edit(embed=answer_embed, content='')
                elif __message == f"{ctx.prefix}hint":
                    num_hints += 1
                    hint = random.choice(hints)
                    hints.remove(hint)
                    embed = discord.Embed(colour=self.bot.colour)
                    embed.set_author(name=f"Hint", icon_url="https://cdn.discordapp.com/emojis/715599637079130202.png?v=1")
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

    def cog_unload(self):
        #close trivia aiohttp session
        self.bot.loop.create_task(self.trivia.close())



def setup(bot):
    bot.add_cog(Games(bot))
