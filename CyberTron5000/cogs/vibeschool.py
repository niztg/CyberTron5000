"""Vibe School is the best Discord Server. Join today!"""

import asyncio
import random

import discord
from discord.ext import commands

from CyberTron5000.utils.checks import check_channel, check_guild_and_admin


# ≫

class VibeSchool(commands.Cog):
    """The best Discord Server. Join today!"""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_check(self, ctx):
        return ctx.guild.id == 734159981208666134
    
    @commands.command(help="info about Vibe School.")
    async def vinfo(self, ctx):
        infoEmbed = discord.Embed(title="Vibe School Info", color=ctx.message.author.color)
        infoEmbed.add_field(name="Visitors",
                            value="People who are visiting, but not official vibers or young. Must take a short quiz before officially starting their journeys.",
                            inline=False)
        infoEmbed.add_field(name="The Young",
                            value="New vibers, hoping to qualify into the vibe program and complete their vibe training",
                            inline=False)
        infoEmbed.add_field(name="Vibe Apprentice",
                            value="Passed their first vibe checks, allowed to prove themselves. Assigned a Vibe Mentor.",
                            inline=False)
        infoEmbed.add_field(name="Vibe", value="Realized their potential, completed the vibe program.")
        infoEmbed.add_field(name="Alumni",
                            value="After being granted the Vibe role, you are granted the Alumni role. Unlike Vibe, Alumni is temporary and only stays with you for as long as you're an alumni/don't have any other advanced roles.",
                            inline=False)
        infoEmbed.add_field(name="Vibe Mentor",
                            value="The teachers of new vibers, here to pass their knowledge and allow new vibers to succeed in the cruel vibe world",
                            inline=False)
        infoEmbed.add_field(name="The Council",
                            value="performs every vibe check, including on the mentors. Bosses of you.", inline=False)
        infoEmbed.add_field(name="Sensei",
                            value="Don't mess with these guys. The mentors of the mentors of the mentors. They know their shit and their vibe.",
                            inline=False)
        infoEmbed.add_field(name="Vibe Adults",
                            value="trust-able and responsible vibers on their way to moving up. Gained after successfully making it through vibe school and finding a post-vibe career path.",
                            inline=False)
        infoEmbed.add_field(name="Seito",
                            value=" Pupils of the Sensei and engage in many special projects. Generally very trustworthy.",
                            inline=False)
        infoEmbed.add_field(name="HEAD COUNCIL",
                            value="Finally, Head Council. This is the most powerful role in the whole establishment, and this person (currently YeetVegetabales) is your boss, on everything. (They are the senate)",
                            inline=False)
        infoEmbed.add_field(name="Moderator", value="Moderator", inline=False)
        infoEmbed.add_field(name="Subreddit Manager", value="Subreddit Moderator", inline=False)
        infoEmbed.add_field(name="Failures", value="Failures", inline=False)
        await ctx.send(embed=infoEmbed)
    
    @commands.command(help="rules for Vibe School")
    async def rules(self, ctx):
        rulesEmbed = discord.Embed(color=ctx.message.author.color, title="Vibe School Rules")
        rulesEmbed.add_field(name="No Cheating",
                             value="Cheating for others will be treated harshly for all parties involved, so do not do it. Vibe School is meant to be fun and competitive, and cheating ruins the purpose of it.")
        rulesEmbed.add_field(name="Don't be a jerk",
                             value="Vibe School is difficult, there is no time to be mean to people",
                             inline=False)
        rulesEmbed.add_field(name="No Slurs",
                             value="We want Vibe School to be a safe and supportive place for everyone, so please- no slurs. A slur will at minimum get you a 14 day ban from this sub and a mute from the discord server. Now you may ask, what is a slur? If you are thinking of a word, and do not know if it is a slur or not, then do not say it. That simple.",
                             inline=False)
        rulesEmbed.add_field(name="Do not incite violence",
                             value="The Vibe School is no place to be violent, you will receive a ban for doing so",
                             inline=False)
        rulesEmbed.add_field(name="No Horny-ness",
                             value="Sheesh bro, take your hormones somewhere else. We do not allow horns or the act of being horny. You could get struck by the horny police.",
                             inline=False)
        rulesEmbed.add_field(name="Have fun and Vibe!",
                             value="Vibe School is meant to be fun, so just be yourself, have fun, and most importantly, VIBE.",
                             inline=False)
        await ctx.send(embed=rulesEmbed)
    
    @commands.command(help="MEE6 commands for Vibe School")
    async def cmds(self, ctx):
        await ctx.send(embed=discord.Embed(title="MEE6 Commands",
                                           description="`!niz`- alerts Sensei Niz\n`!yv` - Alerts YeetVegetabales."
                                                       "\n`!vibecheck` - Checks your vibe\n`!rank` - Check your level.",
                                           color=ctx.message.author.color))
    
    @commands.group(invoke_without_command=True, aliases=['q', 'tq'])
    async def take_quiz(self, ctx):
        cmds = [f"→ `{ctx.prefix}take_quiz {c.name}` - {c.help}" for c in self.bot.get_command("take_quiz").commands]
        await ctx.send("**Quizzes Commands**\n" + "\n".join(cmds))
    
    @take_quiz.command(aliases=['young', 'ty'], invoke_without_command=True)
    @check_channel(channel=738230552959909909)
    async def the_young(self, ctx):
        """Quiz for which you can study in <#687817303177691373> and take in <#687818177773568090>"""
        try:
            ty_questions = ['Who are the Seito?', 'What is the highest role on the Discord server?',
                            'What are two rules?', 'Who is currently occupying the HEAD COUNCIL role?',
                            'What roles do you get after passing Vibe School?',
                            'What is one of the commands that MEE6 can perform?']
            ty_correct = ['Trustworthy vibers raised by Sensei', 'HEAD COUNCIL', 'No being a jerk, No violence',
                          'YeetVegetabales', 'Alumni, Vibe', '!yv']
            ty_wrong = [['Role given after you finish vibe school', 'The second highest ranking role', 'You\'re mom'],
                        ['Sensei', 'The Council', 'discount sensei'],
                        ['No violence, No pinging Sensei', 'No horny-ness, No being stupid',
                         'No violence, No pinging The Council'], ['Sensei Niz', 'kalmdown1', 'Cookie'],
                        ['Vibe', 'Vibe Adult', 'Vibe, Vibe Adult'], ['!sensei', '!senseiniz', '!vibe-check']]
            await ctx.send("You are about to take **The Young Quiz**. Do you wish to proceed? **[yes/no]**")
            message = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
            index = 0
            total = 0
            sleep = 0.5
            if message.content.lower().startswith('y'):
                for question, answer, incorrect in zip(ty_questions, ty_correct, ty_wrong):
                    index += 1
                    pref = "**BONUS:**" if index == len(ty_questions) else f"**Q{index}:**"
                    answers = [a for a in incorrect]
                    answers.append(answer)
                    random.shuffle(answers)
                    x = []
                    for i, v in enumerate(answers, start=1):
                        x.append(f"{i}. **{v}**")
                    await ctx.send(f"{pref} {question}\n_(Type **only** the number)_\n" + "\n".join(x))
                    msg = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
                    if str(answers.index(answer) + 1) == str(msg.content):
                        await ctx.send("Correct!")
                        score = 1 if "bonus" not in pref.lower() else 2
                        total += score
                        await asyncio.sleep(sleep)
                        continue
                    else:
                        await ctx.send(
                            f"Sorry, that's wrong. The correct answer is {answers.index(answer) + 1}, _{answer}_.")
                        await asyncio.sleep(sleep)
                        continue
                p = True if round(total / len(ty_questions) * 100) > 70 else False
                embed = discord.Embed(
                    description=f"Score: **{total}** out of **{len(ty_questions)}**\nPercent: **{round(total / len(ty_questions) * 100)}%**\nPass? {p}",
                    colour=self.bot.colour, title="Test Results").set_footer(text="Note: Bonus questions count as two points.")
                embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                if p:
                    role = discord.utils.get(ctx.guild.roles, name="The Young")
                    a_role = discord.utils.get(ctx.guild.roles, name="Visitors")
                    await ctx.author.add_roles(role)
                    await ctx.author.remove_roles(a_role)
                    await ctx.send("Congrats! You have been given `The Young` role!")
                elif not p:
                    await ctx.send("Sorry, you failed. Try again next time!")
            elif message.content.lower().startswith('n'):
                return await ctx.send("Ok, aborted.")
            else:
                await ctx.send("Booo! Restart!")
        except Exception as er:
            await ctx.send(er)
    
    @take_quiz.command(aliases=['ad', 'adulthood'], invoke_without_command=True)
    @check_channel(channel=738231113696280587)
    async def vibe_adult(self, ctx):
        """Quiz for which you can study in <#687821074200526873> and take in <#687821074200526873>"""
        try:
            ty_questions = ['Who is/are the boss(es) of The Council?',
                            f'Which role manages the Discord server and uses {self.bot.user.mention}?',
                            'Who manage the Subreddit?', 'What colour does the Vibe Mentor role get?',
                            'What job is on the bottom of the hierarchy?', 'What is the job of The Council?']
            ty_correct = ['HEAD COUNCIL', 'Moderator', 'Subreddit Manager', 'Blue', 'Vibe Mentor',
                          'To decide who moves up to what role']
            ty_wrong = [['Sensei', 'Moderator', 'Vibe'], ['Subreddit Manager', 'Subreddit Boss', 'HEAD COUNCIL'],
                        ['The Council', 'Sensei', 'Vibe Adult'], ['Red', 'Purple', 'Peach'],
                        ['Moderator', 'Subreddit Boss', 'Queue Manager'],
                        ['To teach you how to vibe', 'To promote the Discord', 'To promote the subreddit']]
            await ctx.send("You are about to take **Vibe Adulthood Quiz**. Do you wish to proceed? **[yes/no]**")
            message = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
            index = 0
            total = 0
            sleep = 0.5
            if message.content.lower().startswith('y'):
                for question, answer, incorrect in zip(ty_questions, ty_correct, ty_wrong):
                    index += 1
                    pref = "**BONUS:**" if index == len(ty_questions) else f"**Q{index}:**"
                    answers = [a for a in incorrect]
                    answers.append(answer)
                    random.shuffle(answers)
                    x = []
                    for i, v in enumerate(answers, start=1):
                        x.append(f"{i}. **{v}**")
                    await ctx.send(f"{pref} {question}\n_(Type **only** the number)_\n" + "\n".join(x))
                    msg = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
                    if str(answers.index(answer) + 1) == str(msg.content):
                        await ctx.send("Correct!")
                        score = 1 if "bonus" not in pref.lower() else 2
                        total += score
                        await asyncio.sleep(sleep)
                        continue
                    else:
                        await ctx.send(
                            f"Sorry, that's wrong. The correct answer is {answers.index(answer) + 1}, _{answer}_.")
                        await asyncio.sleep(sleep)
                        continue
                p = True if round(total / len(ty_questions) * 100) > 70 else False
                embed = discord.Embed(
                    description=f"Score: **{total}** out of **{len(ty_questions)}**\nPercent: **{round(total / len(ty_questions) * 100)}%**\nPass? {p}",
                    colour=self.bot.colour, title="Test Results").set_footer(text="Note: Bonus questions count as two points.")
                embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                if p:
                    role = discord.utils.get(ctx.guild.roles, name="Vibe Adults")
                    await ctx.author.add_roles(role)
                    await ctx.send("Congrats! You have been given the `Vibe Adults` role!")
                elif not p:
                    await ctx.send("Sorry, you failed. Try again next time!")
            elif message.content.lower().startswith('n'):
                return await ctx.send("Ok, aborted.")
            else:
                await ctx.send("Booo! Restart!")
        except Exception as er:
            await ctx.send(er)
    
    @commands.command(help="Gets you info about Vibe Adulthood")
    @check_channel(channel=738231113696280587)
    async def adinfo(self, ctx):
        adEmbed = discord.Embed(color=0xa30533, title="Job Info")
        adEmbed.add_field(name="Vibe Mentor",
                          value="As the server has no pattern to its growth, Vibe Mentor will always be an open role. You perform the same vibe checks as your mentor did to you, but you DON'T MOVE ANYONE UP. That's The Council's job. You can become Vibe Mentor simply by asking, however usually your own Vibe Mentor or a Councilperson will recommend it for you. Nice blue colour too. This role is the bottom of the post-school job hierarchy.",
                          inline=False)
        adEmbed.add_field(name="Queue Manager",
                          value="A pink role and obligation to post as much as possible on the subreddit. Ignore your morals ;).")
        adEmbed.add_field(name="Subreddit Manager",
                          value="Alongside a nice orangey colour - These guys are the moderators of r/VibeSchool and are in charge of frequently posting, promoting the subreddit, approving posts in new, and answering questions.",
                          inline=False)
        adEmbed.add_field(name="BotStyle",
                          value="A role given to you if you if you have added a bot to the server.",
                          inline=False)
        adEmbed.add_field(name="\n*The roles from now on are Senior Viber roles. The roles before have been Junior.*",
                          value="--------------------------------------------------------------------------------------------",
                          inline=False)
        adEmbed.add_field(name="Management Staff",
                          value="these guys deal with the Vibe School meta - such as how to deal with specific users, big ideas, and new moderators. you can also apply for this one > [here](https://docs.google.com/forms/d/e/1FAIpQLScW5N51sTUpQexDOlxIm3XPS9BPWBJGvM8TxbGXvOytU4yYdg/viewform)",
                          inline=False)
        
        adEmbed.add_field(name="Moderator",
                          value="These guys have a sangria red colour, and a responsibility to use CyberTron5000 to mute, kick and ban people, create new channels, add new features to the server, and make announcements. ",
                          inline=False)
        adEmbed.add_field(name="Bot Dictator",
                          value="Whereas BotStyle is simply for users who add bots, Bot Dicator is for users who's bots have made a meaningful, practical contribution to VibeSchool.",
                          inline=False)
        adEmbed.add_field(name="Head Moderator",
                          value="moderator except more trusted with stuff.",
                          inline=False)
        adEmbed.add_field(name="The Council",
                          value="These guys are the real big shots of the server. They decide on every vibe check beneath them, and vote on very important rules for the subreddit and Discord. Councilpeople usually have many or all of the roles beneath them on the job hierarchy. ",
                          inline=False)
        adEmbed.add_field(name="Overseer",
                          value="Boss of management staff. Closed.",
                          inline=False)
        adEmbed.add_field(name="Subreddit Boss",
                          value="Technically a closed role held by YeetVegetabales. This one person is the boss of the Subreddit managers and takes extra care of the Subreddit. Teal colour.",
                          inline=False)
        adEmbed.add_field(name="HEAD COUNCIL",
                          value="While not a closed role necessarily, only becomes open once the current HEAD COUNCIL resigns. When that happens, a way to organize the next one will be made, but for now, know that this guy is the boss of The Council, and also gets final say on pretty much everything. Currently, it is YeetVegetabales.",
                          inline=False)
        await ctx.send(embed=adEmbed)
    
    @commands.command(help="the eppicest server in the land")
    async def vibe_server (self, ctx):
        embed = discord.Embed(
            colour=self.bot.colour,
            title="join now", url="https://discord.gg/m6mqkPT"
        )
        await ctx.send(embed=embed)
    
    @commands.command(help="Vote when it's voting time")
    async def votev(self, ctx, person, *, reason):
        await ctx.bot.owner.send(f"Hey, {ctx.message.author.display_name} just voted for {person}. Reason:\n```{reason}```")
        await ctx.message.add_reaction(emoji=ctx.tick())
    
    @commands.group(invoke_without_command=True,
                    help="contact management if there's anything you want to say to them")
    async def management(self, ctx, *, message):
        channel = self.bot.get_channel(id=734171313253515274)
        await channel.send(
            f"Hey, {ctx.message.author} contacted you <@&689613285170872575>\n```{message}```")
        await ctx.message.add_reaction(emoji=ctx.tick())
    
    @management.command(invoke_without_command=True, help="reply to someone contacting management")
    @check_channel(channel=734171313253515274)
    async def reply(self, ctx, member: discord.Member, *, message):
        try:
            user = self.bot.get_user(id=member.id)
            await user.send(f"Hey, Management got back to you for {ctx.guild}.\n```{message}```")
            await ctx.message.add_reaction(emoji=ctx.tick())
        except Exception as error:
            await ctx.send(error)
    
    @commands.command(help="ascend someone")
    @check_guild_and_admin(guild=734267872683098122)
    async def ascend(self, ctx, member: discord.Member):
        roles = [role for role in member.roles]
        message = "<@&712341913575096430>"
        embed = discord.Embed(title=f"A new member is ready to ascend!", color=0xff0000,
                              description=f"**Name: {member.display_name}\n\n**USER NEEDS 5 VOTES TO ASCEND!")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"Ascension initiated by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name=f"**Roles ({len(roles) - 1})**",
                        value=" • ".join([role.mention for role in roles[::-1][:10] if role.id != ctx.guild.id]),
                        inline=False)
        embed.add_field(name="**Joined Guild**", value=f"{member.joined_at.strftime('%B %d, %Y')} ", inline=False)
        message = await ctx.send(message, embed=embed)
        for r in ['⬆️', '⬇️']:
            await message.add_reaction(r)
            
    @commands.command()
    async def vibe_suggest(self, ctx, *, message):
        """Suggest something for VIBE SCHOOL's rebuilding!"""
        channel = self.bot.get_channel(734171313253515274)
        await channel.send(f"Suggestion from **{ctx.author}**\n```{message}```")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(VibeSchool(bot))
