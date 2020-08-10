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
from CyberTron5000.utils.checks import check_admin_or_owner, beta_squad

start_time = datetime.datetime.utcnow()

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


class Meta(commands.Cog):
    """Meta Bot commands"""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":tickgreen:732660186560462958"
        self.version = f"{self.client.user.name} Beta v3.0.0"
        self.softwares = ['<:dpy:708479036518694983>', '<:python:706850228652998667>', '<:JSON:710927078513442857>',
                          '<:psql:733848802334736395>']
    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        a = f"**{days}** days\n**{hours}** hours\n**{minutes}** minutes\n**{seconds}** seconds"
        await ctx.send(embed=discord.Embed(description=a, colour=self.client.colour).set_author(
            name=f"I have been up for {str(humanize.naturaltime(datetime.datetime.utcnow() - start_time)).split('ago')[0]}"))
    
    @commands.command(help="Checks the bot's ping.")
    async def ping(self, ctx):
        websocket = round(self.client.latency * 1000, 3)
        start = time.perf_counter()
        embed = discord.Embed(color=self.client.colour,
                              description=f"**Pong! :ping_pong:**\nWebsocket Latency **{websocket}**")
        message = await ctx.send(embed=embed)
        end = time.perf_counter()
        duration = round((end - start) * 1000, 3)
        embed.description += f"\nResponse Time **{duration}**"
        await message.edit(embed=embed)
    
    @commands.command(aliases=["sourcecode", "src"], help="Shows source code for a given command")
    async def source(self, ctx, *, command=None):
        # Code used from Rapptz' RoboDanny GitHub repository provided by the MIT License
        # https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
        # Copyright (c) 2015 Rapptz
        if not command:
            embed = discord.Embed(color=self.client.colour,
                                  title="<:star:737736250718421032> Check out the source code on GitHub!",
                                  url="https://github.com/niztg/CyberTron5000")
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE",
                            value=f"[MIT](https://opensource.org/licenses/MIT)")
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_image(
                url='https://media.discordapp.net/attachments/381963689470984203/740703797843722431/Screen_Shot_2020-08-05_at_6.52.17_PM.png')
            return await ctx.send(embed=embed)
        elif command in ("help", "?"):
            embed = discord.Embed(colour=self.client.colour, title=f"<:star:737736250718421032> Sourcecode for command help/?", url="https://github.com/niztg/CyberTron5000/blob/master/CyberTron5000/cogs/help.py#L9-L126")
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE", value=f"[MIT](https://opensource.org/licenses/MIT)")
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_image(url='https://media.discordapp.net/attachments/381963689470984203/740703797843722431/Screen_Shot_2020-08-05_at_6.52.17_PM.png')
            await ctx.send(embed=embed)
        else:
            cmd = self.client.get_command(command)
            if not cmd:
                return await ctx.send("Command not found.")
            file = cmd.callback.__code__.co_filename
            location = os.path.relpath(file)
            total, fl = __import__('inspect').getsourcelines(cmd.callback)
            ll = fl + (len(total) - 1)
            url = f"https://github.com/niztg/CyberTron5000/blob/master/CyberTron5000/{location}#L{fl}-L{ll}"
            if not cmd.aliases:
                char = '\u200b'
            else:
                char = '/'
            embed = discord.Embed(color=self.client.colour,
                                  title=f"<:star:737736250718421032> Sourcecode for command {cmd.name}{char}{'/'.join(cmd.aliases)}",
                                  url=url)
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE",
                            value=f"[MIT](https://opensource.org/licenses/MIT)")
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_image(
                url='https://media.discordapp.net/attachments/381963689470984203/740703797843722431/Screen_Shot_2020-08-05_at_6.52.17_PM.png')
            await ctx.send(embed=embed)

    @commands.command(help="Shows total lines of code used to make the bot.")
    async def lines(self, ctx):
        await ctx.send(f"**{self.client.user.name}** was made with **{lines_of_code().get('lines'):,}** lines of code!")
    
    async def get_commits(self, limit: int = 3, names: bool = True, author: bool = True):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.github.com/repos/niztg/CyberTron5000/commits") as r:
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
        delta_uptime = datetime.datetime.utcnow() - start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        a = f"**{days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds"
        lines = lines_of_code()
        news = await self.client.pg_con.fetch("SELECT message, number FROM news")
        embed = discord.Embed(colour=self.client.colour)
        embed.set_author(name=f"About {self.version}", icon_url=self.client.user.avatar_url)
        embed.description = f"→ [Invite](https://cybertron-5k.netlify.app/invite) | [Support](https://cybertron-5k.netlify.app/server) | <:github:724036339426787380> [GitHub](https://github.com/niztg/CyberTron5000) | <:cursor_default:734657467132411914>[Website](https://cybertron-5k.netlify.app) | <:karma:704158558547214426> [Reddit](https://reddit.com/r/CyberTron5000)\n"
        embed.description += f"→ Latest Commits: {'|'.join(await self.get_commits(limit=3, author=False, names=False))}\n"
        embed.description += f"→ Used Memory | {cyberformat.bar(stat=psutil.virtual_memory()[2], max=100, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>')}\n→ CPU | {cyberformat.bar(stat=psutil.cpu_percent(), max=100, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>')}"
        embed.description += f"\n→ Uptime | {a}"
        embed.description += f"\n**{lines.get('lines'):,}** lines of code | **{lines.get('files'):,}** files\n{self.softwares[0]} {discord.__version__}\n{self.softwares[1]} {platform.python_version()}"
        embed.add_field(name=f"<:news:730866149109137520> News Update #{news[0][1]}", value=news[0][0], inline=False)
        embed.set_footer(
            text=f"Developed by {str(ctx.bot.owner)} | Bot created {humanize.naturaltime(datetime.datetime.utcnow() - self.client.user.created_at)}",
            icon_url=ctx.bot.owner.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.group(aliases=["n", "changenickname", "nick"], invoke_without_command=True,
                    help="Change the bot's nickname to a custom one.")
    @check_admin_or_owner()
    async def nickname(self, ctx, *, nickname=None):
        if nickname:
            await ctx.guild.me.edit(nick=f"{nickname}")
            await ctx.message.add_reaction(emoji=self.tick)
        else:
            await ctx.guild.me.edit(nick=self.client.user.name)
            await ctx.message.add_reaction(emoji=self.tick)
    
    @nickname.command(invoke_without_command=True, help="Change the bot's nickname back to the default.")
    @check_admin_or_owner()
    async def default(self, ctx):
        await ctx.guild.me.edit(nick=f"{self.client.user.name}")
        await ctx.message.add_reaction(emoji=self.tick)
    
    @nickname.command(invoke_without_command=True, help="Change the bot's nickname to the default, without the prefix.")
    @check_admin_or_owner()
    async def client(self, ctx):
        await ctx.guild.me.edit(nick=self.client.user.name)
        await ctx.message.add_reaction(emoji=self.tick)
    
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def suggest(self, ctx, *, idea):
        """Suggest an idea for the bot."""
        tick = "<:tickgreen:732660186560462958>"
        redx = "<:redx:732660210132451369>"
        sugid = str(uuid4())[:8]
        embed = discord.Embed(title=f"Suggestion → {sugid}", description=f"```diff\n! {idea}\n```",
                              colour=self.client.colour)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Do "suggest follow {sugid}" to follow this suggestion!')
        mes = await self.client.logging_channel.send(embed=embed)
        for r in ['⬆️', '⬇️']:
            await mes.add_reaction(r)
        with open("json_files/suggestions.json", "r") as f:
            res = json.load(f)
        res[str(sugid)] = []
        with open("json_files/suggestions.json", "w") as f:
            json.dump(res, f, indent=4)
        ms = await ctx.send(
            f"Do you want to follow this suggestion? If you follow it, you will recieve updates on it's status.\nIf you want to unfollow this suggestion, do `{ctx.prefix}suggest unfollow {sugid}`.\n{tick} | **Yes**\n{redx} | **No**\n(You have 15 seconds)")
        await self.client.pg_con.execute("INSERT INTO suggestions (msg_id, suggest_id) VALUES ($1, $2)", mes.id, sugid)
        try:
            async with async_timeout.timeout(15):
                await ms.add_reaction(tick)
                await ms.add_reaction(redx)
                r, u = await self.client.wait_for('reaction_add', timeout=15, check=lambda r, u: u.bot is False)
                if r.emoji.name == "tickgreen":
                    with open("json_files/suggestions.json", "r") as f:
                        res = json.load(f)
                    res[str(sugid)].append(ctx.author.id)
                    with open("json_files/suggestions.json", "w") as f:
                        json.dump(res, f, indent=4)
                    await ctx.send("Followed suggestion!")
                else:
                    await ctx.send(
                        f"Ok, suggestion not followed. If you ever want to follow it, simply do `{ctx.prefix}suggest follow {sugid}`")
        except asyncio.TimeoutError:
            await ms.edit(content=f"You ran out of time! Suggestion not followed. If you want to follow this suggestion, do `{ctx.prefix}suggest follow {sugid}`")
            if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
                await ms.clear_reactions()
    
    @suggest.command()
    async def follow(self, ctx, id: str):
        """Follow a suggestion"""
        try:
            with open("json_files/suggestions.json", "r") as f:
                res = json.load(f)
            res[str(id)].append(ctx.author.id)
            with open("json_files/suggestions.json", "w") as f:
                json.dump(res, f, indent=4)
            await ctx.send(f"You have successfully followed suggestion `{id}`")
        except KeyError:
            await ctx.send("That suggestion was not found!")
    
    @suggest.command()
    async def unfollow(self, ctx, id: str):
        """Unfollow a suggestion"""
        try:
            with open("json_files/suggestions.json", "r") as f:
                res = json.load(f)
            try:
                index = res[str(id)].index(ctx.author.id)
            except (ValueError, KeyError):
                return await ctx.send("That suggestion was not found, or you aren't following it!")
            res[str(id)].pop(index)
            with open("json_files/suggestions.json", "w") as f:
                json.dump(res, f, indent=4)
            await ctx.send(f"You have successfully unfollowed suggestion `{id}`")
        except KeyError:
            await ctx.send("That suggestion was not found!")
    
    @suggest.command()
    @commands.is_owner()
    async def resolve(self, ctx, id: str, *, reason):
        data = await self.client.pg_con.fetch("SELECT msg_id FROM suggestions WHERE suggest_id = $1", id)
        if not data:
            return await ctx.send("Not a valid suggestion.")
        msg = await ctx.fetch_message(data[0][0])
        embed = msg.embeds[0]
        embed.add_field(name=f"Reply from {ctx.author}", value=reason)
        await msg.edit(embed=embed)
        with open('json_files/suggestions.json', 'r') as f:
            res = json.load(f)
        for i in res[str(id)]:
            a = self.client.get_user(i) or await self.client.fetch_user(i)
            await a.send(content=f"Suggestion **{id}** has been resolved!", embed=embed)
        res.pop(str(id))
        with open("json_files/suggestions.json", "w") as f:
            json.dump(res, f, indent=4)
        await self.client.pg_con.execute("DELETE FROM suggestions WHERE suggest_id = $1", id)
    
    @suggest.command(invoke_without_command=True)
    async def error(self, ctx, *, error):
        """Report an error for this bot."""
        await ctx.bot.owner.send(f"You should fix ```{error}```")
        await ctx.message.add_reaction(emoji=":tickgreen:732660186560462958")
    
    @commands.command(aliases=['stats'])
    async def statistics(self, ctx):
        """Shows you statistics."""
        stats = lines_of_code()
        embed = discord.Embed(colour=ctx.bot.colour)
        embed.set_author(name=f"Stats for {ctx.me.name}", icon_url=ctx.me.avatar_url)
        embed.description = f"**{stats.get('lines'):,}** lines of code | **{stats.get('files')}** files"
        embed.add_field(name="Statistics", value=f"<:class:735360032434290830> Classes: **{stats.get('classes'):,}**\n<:function:735517201561288775> Functions: **{stats.get('functions'):,}**\n<:coroutine:735520608183648337> Coroutines: **{stats.get('coroutine'):,}**\n💬 Comments: **{stats.get('comments'):,}**")
        embed.add_field(name="\u200b", value=f'<:member:731190477927219231> Users: **{len(self.client.users):,}**\n<:Discord:735530547992068146> Servers: **{len(self.client.guilds)}**\n<:text_channel:703726554018086912> Channels: **{len([*self.client.get_all_channels()]):,}**\n<:emoji:734231060069613638> Emojis: **{len(self.client.emojis):,}**')
        await ctx.send(embed=embed)
    
    @commands.command()
    async def credits(self, ctx):
        """The amazing peeps who make ct5k what it is"""
        embed = discord.Embed(colour=self.client.colour)
        embed.set_author(name=f"The People who make {self.client.user.name} what it is today!",
                         icon_url=self.client.user.avatar_url)
        embed.description = f"<@!561688948259422228> - Thank you for drawing {self.client.user.name}'s amazing avatar!\n\n"
        embed.description += f"<@!357918459058978816> - Thank you for helping me in the beginning and teaching me the ropes!\n[His Bot](https://discord.com/oauth2/authorize?client_id=675542011457044512&permissions=1611000896&scope=bot) | [GitHub](https://github.com/DankDumpster) | [Support Server](https://discord.com/invite/TWjxyhC)\n\n"
        embed.description += f"<@!574870314928832533> - Thank you for helping and giving inspiration for many commands on the bot!\n[Their Bot](https://discord.com/oauth2/authorize?client_id=628824408521441291&scope=bot&permissions=1476521159) | [GitHub](https://github.com/spinfish) | [Support Server](https://discord.gg/q3eVHeU)\n\n"
        embed.description += f"<@!491174779278065689> - Thank you for helping a bunch on the bot and inspiring the Images cog!\n[His Bot](https://discord.com/oauth2/authorize?client_id=675589737372975124&permissions=1611000896&scope=bot) | [GitHub](https://github.com/Daggy1234) | [Support Server](https://discord.com/invite/5Y2ryNq)"
        embed.add_field(name="And thanks to the Beta Squad for testing ct5k's beta commands!",
                        value='\n'.join([f'<@{a}>' for a in beta_squad]))
        await ctx.send(embed=embed)
    
    @commands.command()
    async def invite(self, ctx):
        """Invite me to your server!"""
        embed = discord.Embed(colour=self.client.colour)
        embed.add_field(name="Invite the Bot!", value=f"[`Permissions: 104189632`]({self.client.logging['invite']}) <:star:737736250718421032>\n[`Permissions: 8 (Admin)`](https://discord.com/api/oauth2/authorize?client_id=697678160577429584&permissions=8&scope=bot)\n[`Permissions: 0`](https://discord.com/oauth2/authorize?client_id=697678160577429584&scope=bot&permissions=0)\n", inline=False)
        embed.add_field(name="Other", value=f"[`Chose Your Own`](https://discord.com/api/oauth2/authorize?client_id=697678160577429584&permissions=2147483639&scope=bot)", inline=False)
        embed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(content=f"**{ctx.author}** | https://discord.com/oauth2/authorize?client_id=697678160577429584&scope=bot&permissions=104189632", embed=embed)
    
    @commands.command()
    async def support(self, ctx):
        """Join our help server!"""
        embed = discord.Embed(colour=self.client.colour)
        embed.set_author(name="Join the Support Server!", url=self.client.logging['support'])
        embed.description = f"[`Join Today!`]({self.client.logging['support']}) <:star:737736250718421032>"
        embed.add_field(name=f"Emote Servers", value=f"\n".join([f"<:emoji:734231060069613638> [`{key}`]({value})" for key, value in self.client.logging['servers'].items()]))
        embed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(content=f"**{ctx.author}** | https://discord.com/invite/2fxKxJH", embed=embed)
        
    @commands.group(invoke_without_command=True, aliases=['git'])
    async def github(self, ctx):
        """View the code for CyberTron5000!"""
        embed = discord.Embed(color=self.client.colour,
                              title="<:star:737736250718421032> Check out the source code on GitHub!",
                              url=self.client.logging['github'])
        embed.description = "Star the GitHub repository to support the bot!"
        embed.add_field(name="<:license:737733205645590639> LICENSE", value=f"[MIT](https://opensource.org/licenses/MIT)")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_image(
            url='https://media.discordapp.net/attachments/381963689470984203/740703797843722431/Screen_Shot_2020-08-05_at_6.52.17_PM.png')
        await ctx.send(embed=embed)
        
    @github.command(name='commits')
    @commands.is_owner()
    async def _git_commits(self, ctx, limit: int = 5):
        """Shows you recent github commits"""
        if limit < 1 or limit > 15:
            return await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, limit must be greater than 0 and less than 16!")
        commits = [f"{index}. {commit}" for index, commit in
                   enumerate(await self.get_commits(limit, author=False, names=True), 1)]
        await ctx.send(embed=discord.Embed(description="\n".join(commits), colour=self.client.colour).set_author(
            name=f"Last {limit} GitHub Commit(s) for CyberTron5000",
            icon_url="https://www.pngjoy.com/pngl/52/1164606_telegram-icon-github-icon-png-white-png-download.png",
            url=self.client.logging['github']))
        
    @github.command(aliases=['repo'])
    async def repository(self, ctx, repository):
        """View a github repository"""
        embed = discord.Embed(colour=self.client.colour)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.github.com/repos/{repository}") as r1, cs.get(f"https://api.github.com/users/{repository.split('/')[0]}") as r2:
                if r1.status != 200 or r2.status != 200:
                    return await ctx.send(f"Repository not found.")
                res1 = await r1.json()
                res2 = await r2.json()
                await cs.close()
        embed.set_author(name=f'{res1.get("full_name")}', icon_url=res2.get("avatar_url"), url=res1.get("svn_url"))
        embed.description = res1.get("description") or '' + "\n"
        stars = res1.get("stargazers_count")
        watchers = res1.get("subscribers_count")
        language = res1.get("language")
        license = res1.get("license")
        forks = res1.get("forks")
        created = datetime.datetime(*s(str(res1.get('created_at'))[:-1], "%Y-%m-%dT%H:%M:%S")[:6])
        embed.description += f"<:author:738185776642261022> **{res1.get('full_name').split('/')[0]}**\n"
        embed.description += f"<:clock:738186842343735387> **{humanize.naturaltime(datetime.datetime.utcnow()-created)}**\n"
        embed.description += f"<:star:737736250718421032> **{stars:,}**\n<:watchers:738173064130461727> **{watchers:,}**\n"
        embed.description += f"<:fork:738179007295782993> **{forks:,}**\n"
        if license:
            embed.description += f"<:license:738176207895658507> **{license['spdx_id']}**\n"
        embed.set_footer(text=f"Written in {language}")
        await ctx.send(embed=embed)
     
    @commands.command()
    async def news(self, ctx):
        """View the current news."""
        embed = discord.Embed(colour=self.client.colour)
        news = await self.client.pg_con.fetch("SELECT message, number FROM news")
        if not news:
            embed.description = "There is no news currently. Come back soon."
        else:
            embed.description = news[0][0]
            embed.set_author(name=f"News update #{news[0][1]} for {self.client.user.name}",
                             icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def actual_users(self, ctx):
        """Shows the bot's user count excluding bot servers"""
        totals = []
        for g in [336642139381301249, 450594207787384832, 733064960241958982]:
            totals.append(ctx.bot.get_guild(g).member_count)
        total = len([u for u in ctx.bot.users]) - sum(totals)
        await ctx.send(f"Aside from bot servers, {self.client.user.name} has a total of **{total:,}** users.")

def setup(client):
    client.add_cog(Meta(client))
