"""
For general bot commands, basic/meta stuff.
"""

import asyncio
import datetime
import json
import os
import platform
import time
from time import strptime as s
from uuid import uuid4

import aiohttp
import async_timeout
import discord
import humanize
import psutil
from discord.ext import commands

from CyberTron5000.utils import cyberformat
from CyberTron5000.utils.checks import beta_squad


# ≫
def lines_of_code():
    """
    I did not write this code.
    This code was taken off of a tag in discord.gg/dpy owned by Dutchy#6127
    I don't know if this is licensed
    but alas
    :return:
    """
    import pathlib
    p = pathlib.Path('./')
    cm = cr = fn = cl = ls = fc = 0
    for f in p.rglob('*.py'):
        if str(f).startswith("venv"):
            continue
        fc += 1
        with f.open() as of:
            for l in of.readlines():
                l = l.strip()
                if l.startswith('class'):
                    cl += 1
                if l.startswith('def'):
                    fn += 1
                if l.startswith('async def'):
                    cr += 1
                if '#' in l:
                    cm += 1
                ls += 1
    return {
        "comments": cm,
        "coroutine": cr,
        "functions": fn,
        "classes": cl,
        "lines": ls,
        "files": fc
    }

lines = lines_of_code()


class Meta(commands.Cog):
    """Meta Bot commands"""

    def __init__(self, bot):
        self.bot = bot
        self.version = f"{self.bot.user.name} Beta v3.0.0"
        self.softwares = ['<:dpy:708479036518694983>', '<:python:706850228652998667>', '<:JSON:710927078513442857>',
                          '<:psql:733848802334736395>']

    @commands.command()
    async def uptime(self, ctx):
        uptime = []
        for key, value in self.bot.uptime.items():
            uptime.append(f'**{value}** {key}')
        await ctx.send(embed=discord.Embed(description='\n'.join(uptime), colour=self.bot.colour).set_author(name=f"I have been up for {str(humanize.naturaltime(datetime.datetime.utcnow() - self.bot.start_time)).split('ago')[0]}"))

    @commands.command()
    async def ping(self, ctx):
        """Shows you the bot's latency"""

        def check_health(i: float, vals: tuple = (150, 400)):
            if i <= vals[0]:
                return '<:online:726127263401246832>'
            elif i <= vals[1]:
                return '<:idle:726127192165187594>'
            else:
                return '<:dnd:726127192001478746>'

        websocket = round(self.bot.latency * 1000, 3)
        start = time.perf_counter()
        message = f"{check_health(websocket)} <:wumpus:742965982640865311> Websocket Latency `{websocket}` ms"
        msg = await ctx.send(message)
        end = time.perf_counter()
        duration = round((end - start) * 1000, 3)
        message += f"\n{check_health(duration, (200, 500))} <:clock:738186842343735387> Response Time `{duration}` ms"
        await msg.edit(content=message)
        db_start = time.perf_counter()
        await self.bot.db.fetch("SELECT * FROM news")
        db_end = time.perf_counter()
        db_dur = round((db_end-db_start)*1000, 3)
        message += f"\n{check_health(db_dur, (5, 15))} {self.softwares[3]} Database Latency `{db_dur}` ms"
        # thanks to dutchy for db latency idea
        await msg.edit(content=message)

    @commands.command(aliases=["sourcecode", "src"], help="Shows source code for a given command")
    async def source(self, ctx, *, command=None):
        # Lines 137-141 used from Rapptz' RoboDanny GitHub repository provided by the MIT License
        # https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
        # Copyright (c) 2015 Rapptz
        if not command:
            embed = discord.Embed(color=self.bot.colour,
                                  title="<:star:737736250718421032> Check out the source code on GitHub!",
                                  url="https://github.com/niztg/CyberTron5000")
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE",
                            value=f"[MIT](https://opensource.org/licenses/MIT)")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_image(
                url='https://media.discordapp.net/attachments/381963689470984203/740703797843722431/Screen_Shot_2020-08-05_at_6.52.17_PM.png')
            return await ctx.send(embed=embed)
        elif command in ("help", "?"):
            embed = discord.Embed(colour=self.bot.colour,
                                  title=f"<:star:737736250718421032> Sourcecode for command help/?",
                                  url="https://github.com/niztg/CyberTron5000/blob/master/CyberTron5000/cogs/help.py#L9-L126")
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE",
                            value=f"[MIT](https://opensource.org/licenses/MIT)")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_image(
                url='https://media.discordapp.net/attachments/381963689470984203/740703797843722431/Screen_Shot_2020-08-05_at_6.52.17_PM.png')
            await ctx.send(embed=embed)
        else:
            cmd = self.bot.get_command(command)
            if not cmd:
                return await ctx.send("Command not found.")
            file = cmd.callback.__code__.co_filename
            location = os.path.relpath(file)
            total, fl = __import__('inspect').getsourcelines(cmd.callback)
            ll = fl + (len(total) - 1)
            url = f"https://github.com/niztg/CyberTron5000/blob/master/{location}#L{fl}-L{ll}"
            if not cmd.aliases:
                char = '\u200b'
            else:
                char = '/'
            embed = discord.Embed(color=self.bot.colour,
                                  title=f"<:star:737736250718421032> Sourcecode for command {cmd.name}{char}{'/'.join(cmd.aliases)}",
                                  url=url)
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE",
                            value=f"[MIT](https://opensource.org/licenses/MIT)")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_image(
                url='https://media.discordapp.net/attachments/381963689470984203/740703797843722431/Screen_Shot_2020-08-05_at_6.52.17_PM.png')
            await ctx.send(embed=embed)

    @commands.command(help="Shows total lines of code used to make the bot.")
    async def lines(self, ctx):
        await ctx.send(f"**{self.bot.user.name}** was made with **{lines.get('lines'):,}** lines of code!")

    async def get_commits(self, limit: int = 3, names: bool = True, author: bool = True):
        async with self.bot.session.get("https://api.github.com/repos/niztg/CyberTron5000/commits") as r:
            res = await r.json()
            commits = []
            for item in res:
                msg = f"[`{item['sha'][0:7]}`](https://github.com/niztg/CyberTron5000/commit/{item['sha']})"
                if names:
                    msg += f" {item['commit']['message']}"
                if author:
                    msg += f" - {item['commit']['committer']['name']}"
                commits.append(msg)
            return commits[:limit]

    @commands.command(aliases=['ab', 'info'])
    async def about(self, ctx):
        """Shows you information regarding the bot"""
        async with ctx.typing():
            uptime = []
            for key, value in self.bot.uptime.items():
                uptime.append(f'**{value}** {key}')
            uptime = ', '.join(uptime)
            news = await self.bot.db.fetch("SELECT message, number FROM news")
            embed = discord.Embed(colour=self.bot.colour)
            embed.set_author(name=f"About {self.version}", icon_url=self.bot.user.avatar_url)
            embed.description = f"→ [Invite](https://cybertron-5k.netlify.app/invite) | [Support](https://cybertron-5k.netlify.app/server) | <:github:724036339426787380> [GitHub](https://github.com/niztg/CyberTron5000) | <:cursor_default:734657467132411914>[Website](https://cybertron-5k.netlify.app) | <:karma:704158558547214426> [Reddit](https://reddit.com/r/CyberTron5000)\n"
            embed.description += f"→ Latest Commits: {'|'.join(await self.get_commits(limit=3, author=False, names=False))}\n"
            embed.description += f"→ Used Memory | {cyberformat.bar(stat=psutil.virtual_memory()[2], max=100, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>')}\n→ CPU | {cyberformat.bar(stat=psutil.cpu_percent(), max=100, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>')}"
            embed.description += f"\n→ Uptime | {uptime}"
            embed.description += f"\n**{lines.get('lines'):,}** lines of code | **{lines.get('files'):,}** files\n{self.softwares[0]} {discord.__version__}\n{self.softwares[1]} {platform.python_version()}"
            embed.add_field(name=f"<:news:730866149109137520> News Update #{news[0][1]}", value=news[0][0], inline=False)
            embed.set_footer(
                text=f"Developed by {str(ctx.bot.owner)} | Bot created {humanize.naturaltime(datetime.datetime.utcnow() - self.bot.user.created_at)}",
                icon_url=ctx.bot.owner.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def suggest(self, ctx, *, idea):
        """Suggest an idea for the bot."""
        sugid = str(uuid4())[:8]
        embed = discord.Embed(title=f"Suggestion → {sugid}", description=f"```fix\n{idea}```",
                              colour=self.bot.colour)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Do "suggest follow {sugid}" to follow this suggestion!')
        mes = await self.bot.logging_channel[2].send(embed=embed)
        for r in ['⬆️', '⬇️']:
            await mes.add_reaction(r)
        with open("CyberTron5000/json_files/suggestions.json", "r") as f:
            res = json.load(f)
        res[str(sugid)] = []
        with open("CyberTron5000/json_files/suggestions.json", "w") as f:
            json.dump(res, f, indent=4)
        ms = await ctx.send(
            f"Do you want to follow this suggestion? If you follow it, you will recieve updates on it's status.\nIf you want to unfollow this suggestion, do `{ctx.prefix}suggest unfollow {sugid}`.\n{ctx.tick()} | **Yes**\n{ctx.tick(False)} | **No**\n(You have 15 seconds)")
        await self.bot.db.execute("INSERT INTO suggestions (msg_id, suggest_id) VALUES ($1, $2)", mes.id, sugid)
        try:
            async with async_timeout.timeout(15):
                for emoji in (ctx.tick(True), ctx.tick(False)):
                    await ms.add_reaction(emoji)
                r, u = await self.bot.wait_for('reaction_add', timeout=15, check=lambda r, u: u.bot is False)
                if r.emoji.name == "tickgreen":
                    with open("CyberTron5000/json_files/suggestions.json", "r") as f:
                        res = json.load(f)
                    res[str(sugid)].append(ctx.author.id)
                    with open("CyberTron5000/json_files/suggestions.json", "w") as f:
                        json.dump(res, f, indent=4)
                    await ctx.send("Followed suggestion!")
                else:
                    await ctx.send(
                        f"Ok, suggestion not followed. If you ever want to follow it, simply do `{ctx.prefix}suggest follow {sugid}`")
        except asyncio.TimeoutError:
            await ms.edit(
                content=f"You ran out of time! Suggestion not followed. If you want to follow this suggestion, do `{ctx.prefix}suggest follow {sugid}`")
        if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
            await ms.clear_reactions()

    @suggest.command()
    async def follow(self, ctx, id: str):
        """Follow a suggestion"""
        try:
            with open("CyberTron5000/json_files/suggestions.json", "r") as f:
                res = json.load(f)
            res[str(id)].append(ctx.author.id)
            with open("CyberTron5000/json_files/suggestions.json", "w") as f:
                json.dump(res, f, indent=4)
            await ctx.send(f"You have successfully followed suggestion `{id}`")
        except KeyError:
            await ctx.send("That suggestion was not found!")

    @suggest.command()
    async def unfollow(self, ctx, id: str):
        """Unfollow a suggestion"""
        try:
            with open("CyberTron5000/json_files/suggestions.json", "r") as f:
                res = json.load(f)
            try:
                index = res[str(id)].index(ctx.author.id)
            except (ValueError, KeyError):
                return await ctx.send("That suggestion was not found, or you aren't following it!")
            res[str(id)].pop(index)
            with open("CyberTron5000/json_files/suggestions.json", "w") as f:
                json.dump(res, f, indent=4)
            await ctx.send(f"You have successfully unfollowed suggestion `{id}`")
        except KeyError:
            await ctx.send("That suggestion was not found!")

    @suggest.command()
    @commands.is_owner()
    async def resolve(self, ctx, id: str, *, reason):
        data = await self.bot.db.fetch("SELECT msg_id FROM suggestions WHERE suggest_id = $1", id)
        if not data:
            return await ctx.send("Not a valid suggestion.")
        msg = await ctx.fetch_message(data[0][0])
        embed = msg.embeds[0]
        embed.add_field(name=f"Reply from {ctx.author}", value=reason)
        await msg.edit(embed=embed)
        with open('CyberTron5000/json_files/suggestions.json', 'r') as f:
            res = json.load(f)
        for i in res[str(id)]:
            a = self.bot.get_user(i) or await self.bot.fetch_user(i)
            await a.send(content=f"Suggestion **{id}** has been resolved!", embed=embed)
        res.pop(str(id))
        with open("CyberTron5000/json_files/suggestions.json", "w") as f:
            json.dump(res, f, indent=4)
        await self.bot.db.execute("DELETE FROM suggestions WHERE suggest_id = $1", id)

    @suggest.command(invoke_without_command=True)
    async def error(self, ctx, *, error):
        """Report an error for this bot."""
        await ctx.bot.owner.send(f"You should fix ```{error}```")
        await ctx.message.add_reaction(emoji=ctx.tick())

    @commands.command(aliases=['stats'])
    async def statistics(self, ctx):
        """Shows you statistics."""
        embed = discord.Embed(colour=ctx.bot.colour)
        embed.set_author(name=f"lines for {ctx.me.name}", icon_url=ctx.me.avatar_url)
        embed.description = f"**{lines.get('lines'):,}** lines of code | **{lines.get('files')}** files"
        embed.add_field(name="Statistics",
                        value=f"<:class:735360032434290830> Classes: **{lines.get('classes'):,}**\n<:function:735517201561288775> Functions: **{lines.get('functions'):,}**\n<:coroutine:735520608183648337> Coroutines: **{lines.get('coroutine'):,}**\n💬 Comments: **{lines.get('comments'):,}**")
        embed.add_field(name="\u200b",
                        value=f'<:member:731190477927219231> Users: **{len(self.bot.users):,}**\n<:Discord:735530547992068146> Servers: **{len(self.bot.guilds)}**\n<:text_channel:703726554018086912> Channels: **{len([*self.bot.get_all_channels()]):,}**\n<:emoji:734231060069613638> Emojis: **{len(self.bot.emojis):,}**')
        await ctx.send(embed=embed)

    @commands.command()
    async def credits(self, ctx):
        """The amazing peeps who make ct5k what it is"""
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name=f"The People who make {self.bot.user.name} what it is today!",
                         icon_url=self.bot.user.avatar_url)
        embed.description = f"<@!561688948259422228> - Thank you for drawing {self.bot.user.name}'s amazing avatar!\n\n"
        embed.description += f"<@!357918459058978816> - Thank you for helping me in the beginning and teaching me the ropes!\n[His Bot](https://discord.com/oauth2/authorize?client_id=675542011457044512&permissions=1611000896&scope=bot) | [GitHub](https://github.com/DankDumpster) | [Support Server](https://discord.com/invite/TWjxyhC)\n\n"
        embed.description += f"<@!491174779278065689> - Thank you for helping a bunch on the bot and inspiring the Images cog!\n[His Bot](https://discord.com/oauth2/authorize?client_id=675589737372975124&permissions=1611000896&scope=bot) | [GitHub](https://github.com/Daggy1234) | [Support Server](https://discord.com/invite/5Y2ryNq)"
        embed.add_field(name="And thanks to the Beta Squad for testing ct5k's beta commands!",
                        value='\n'.join([f'<@{a}>' for a in beta_squad]))
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Invite me to your server!"""
        await ctx.send(content=f"**{ctx.author}** | https://discord.com/oauth2/authorize?client_id=697678160577429584&scope=bot&permissions=104189632")

    @commands.command()
    async def support(self, ctx):
        """Join our help server!"""
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name="Join the Support Server!", url=self.bot.logging['support'])
        embed.description = f"[`Join Today!`]({self.bot.logging['support']}) <:star:737736250718421032>"
        embed.add_field(name=f"Emote Servers", value=f"\n".join(
            [f"<:emoji:734231060069613638> [`{key}`]({value})" for key, value in
             self.bot.logging['servers'].items()]))
        embed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(content=f"**{ctx.author}** | https://discord.com/invite/2fxKxJH", embed=embed)

    @commands.group(invoke_without_command=True, aliases=['git'])
    async def github(self, ctx):
        """View the code for CyberTron5000!"""
        embed = discord.Embed(color=self.bot.colour,
                              title="<:star:737736250718421032> Check out the source code on GitHub!",
                              url=self.bot.logging['github'])
        embed.description = "Star the GitHub repository to support the bot!"
        embed.add_field(name="<:license:737733205645590639> LICENSE",
                        value=f"[MIT](https://opensource.org/licenses/MIT)")
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_image(
            url='https://media.discordapp.net/attachments/381963689470984203/740703797843722431/Screen_Shot_2020-08-05_at_6.52.17_PM.png')
        await ctx.send(embed=embed)

    @github.command(name='commits')
    async def _git_commits(self, ctx, limit: int = 5):
        """Shows you recent github commits"""
        if limit < 1 or limit > 15:
            return await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, limit must be greater than 0 and less than 16!")
        commits = [f"{index}. {commit}" for index, commit in
                   enumerate(await self.get_commits(limit, author=False, names=True), 1)]
        await ctx.send(embed=discord.Embed(description="\n".join(commits), colour=self.bot.colour).set_author(
            name=f"Last {limit} GitHub Commit(s) for CyberTron5000",
            icon_url="https://www.pngjoy.com/pngl/52/1164606_telegram-icon-github-icon-png-white-png-download.png",
            url=self.bot.logging['github']))

    @github.command(aliases=['repo'])
    async def repository(self, ctx, repository):
        """View a github repository"""
        embed = discord.Embed(colour=self.bot.colour)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.github.com/repos/{repository}") as r1, cs.get(
                    f"https://api.github.com/users/{repository.split('/')[0]}") as r2:
                if r1.status != 200 or r2.status != 200:
                    return await ctx.send(f"Repository not found.")
                res1 = await r1.json()
                res2 = await r2.json()
        embed.set_author(name=f'{res1.get("full_name")}', icon_url=res2.get("avatar_url"), url=res1.get("svn_url"))
        embed.description = res1.get("description") or '' + "\n"
        stars = res1.get("stargazers_count")
        watchers = res1.get("subscribers_count")
        language = res1.get("language")
        license = res1.get("license")
        forks = res1.get("forks")
        created = datetime.datetime(*s(str(res1.get('created_at'))[:-1], "%Y-%m-%dT%H:%M:%S")[:6])
        embed.description += f"<:author:738185776642261022> **{res1.get('full_name').split('/')[0]}**\n"
        embed.description += f"<:clock:738186842343735387> **{humanize.naturaltime(datetime.datetime.utcnow() - created)}**\n"
        embed.description += f"<:star:737736250718421032> **{stars:,}**\n<:watchers:738173064130461727> **{watchers:,}**\n"
        embed.description += f"<:fork:738179007295782993> **{forks:,}**\n"
        if license:
            embed.description += f"<:license:738176207895658507> **{license['spdx_id']}**\n"
        embed.set_footer(text=f"Written in {language}")
        await ctx.send(embed=embed)

    @commands.command()
    async def news(self, ctx):
        """View the current news."""
        embed = discord.Embed(colour=self.bot.colour)
        news = await self.bot.db.fetch("SELECT message, number FROM news")
        if not news:
            embed.description = "There is no news currently. Come back soon."
        else:
            embed.description = news[0][0]
            embed.set_author(name=f"News update #{news[0][1]} for {self.bot.user.name}",
                             icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Meta(bot))
