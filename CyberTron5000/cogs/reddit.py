import datetime
import random

import aiohttp
import discord
import humanize
from discord.ext import commands

from CyberTron5000.utils import paginator
from CyberTron5000.utils.lists import REDDIT_EMOJIS


class Reddit(commands.Cog):
    """Commands interacting with the Reddit API."""

    def __init__(self, bot):
        self.bot = bot
        self.up = "<:upvote:718895913342337036>"
        self.share = "<:share:730823872265584680>"

    # noinspection PyBroadException

    async def cakeday(self, u: str) -> bool:
        async with aiohttp.ClientSession().get(f'https://www.reddit.com/user/{u}/about/.json') as re:
            k = await re.json()
        created = datetime.datetime.utcfromtimestamp(k['data']['created_utc'])
        today = datetime.datetime.utcnow()
        return (created.month, created.day) == (today.month, today.day)

    @commands.command(help="Shows your Reddit Stats.", aliases=['rs', 'karma', 'redditor'])
    async def redditstats(self, ctx, user):
        trophies = []
        td = {
            True: "<:on:732805104620797965>",
            False: "<:off:732805190582927410>"
        }
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/user/{user}/trophies/.json") as r:
                    res = await r.json()
                async with cs.get(f"https://www.reddit.com/user/{user}/about/.json") as re:
                    k = await re.json()
                await cs.close()
                if r.status != 200 or re.status != 200:
                    if r.status or re.status == 400:
                        custom_message = " Redditor not found. "
                    else:
                        custom_message = "\u200b"
                    return await ctx.send(
                        f"Whoops, something went wrong.{custom_message}Error Codes: {r.status}, {re.status}")
            for item in res['data']['trophies']:
                try:
                    trophies.append(REDDIT_EMOJIS[item['data']['name']])
                except KeyError:
                    print(f"{item['data']['name']} not in trophies list!")
            final = []
            for i in trophies:
                if i not in final:
                    final.append(i)
            cake = " <:cakeday:736660679938932876>" if await self.cakeday(user) else ''
            icon = k['data']['icon_img']
            icon = icon.split("?")[0]
            banner = k['data']['subreddit']['banner_img']
            banner = banner.split("?")[0]
            embed = discord.Embed(color=self.bot.colour)
            embed.set_thumbnail(url=icon)
            embed.url = f"https://reddit.com/user/{user}"
            embed.set_author(name=f"{k['data']['subreddit']['title']}",
                             url=f"https://reddit.com/user/{user}") if f"{k['data']['subreddit']['title']}" else None
            embed.title = k['data']['name'] + cake
            embed.description = f"<:karma:704158558547214426> **{k['data']['link_karma'] + k['data']['comment_karma']:,}** | 🔗 **{k['data']['link_karma']:,}** 💬 **{k['data']['comment_karma']:,}**"
            embed.description += f"\n<:asset:734531316741046283> [Icon URL]({icon})"
            if banner:
                embed.description += f" | [Banner URL]({banner})"
            embed.description += "\n" + ' '.join(final)
            dt = datetime.datetime.utcfromtimestamp(k['data']['created_utc'])
            created = humanize.naturaltime(datetime.datetime.utcnow() - dt)
            embed.add_field(name="Account Settings",
                            value=f'{td[k["data"]["verified"]]} **Verified**\n{td[k["data"]["is_mod"]]} **Is Mod**\n{td[k["data"]["hide_from_robots"]]} **Hide From Robots**\n{td[k["data"]["has_subscribed"]]} **Has Subscribed**')
            embed.set_footer(text=f'Account created {created}')
            await ctx.send(embed=embed)

    @commands.command(aliases=['m'], help="Shows you a meme from some of reddit's dankest places (and r/memes)")
    async def meme(self, ctx):
        subreddit = random.choice(
            ['memes', 'dankmemes', 'okbuddyretard', 'memeeconomy', 'dankexchange', 'pewdiepiesubmissions',
             'wholesomememes'])
        posts = []
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/r/{subreddit}/hot.json", params={'limit': 100}) as r:
                    res = await r.json()
                await cs.close()
                for i in res['data']['children']:
                    posts.append(i['data'])
                s = random.choice([p for p in posts if not p['is_self'] and not p['stickied']])
                embed = discord.Embed(title=str(s['title']), colour=self.bot.colour,
                                      url=f"https://reddit.com/{s['permalink']}",
                                      description=f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**")
                embed.set_author(name=s['author'])
                embed.set_footer(text=f"{s['upvote_ratio'] * 100:,}% upvote ratio | posted to r/{s['subreddit']}")
                embed.set_image(url=s['url'])
                return await ctx.send(embed=embed) if not s['over_18'] or s[
                    'over_18'] and ctx.channel.is_nsfw() else await ctx.send(
                    f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")

    @commands.command(aliases=['iu'], help="Shows you the banner or icon of a subreddit (on old Reddit).")
    async def icon(self, ctx, subreddit, choice="icon"):
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://reddit.com/r/{subreddit}/about/.json") as r:
                    res = await r.json()
                await cs.close()
                data = res['data']
            icon = data['community_icon'].split("?")[0]
            banner = data['banner_background_image'].split("?")[0]
            choices = ['banner', 'icon']
            images = [banner, icon]
            if choice not in choices:
                return await ctx.send(f"Error! Please chose between {' or '.join([f'`{a}`' for a in choices])}!")
            await ctx.send(embed=discord.Embed(colour=self.bot.colour, title=f'r/{subreddit}',
                                               url=images[choices.index(choice)]).set_image(
                url=images[choices.index(choice)]))

    @commands.command(aliases=['mod'])
    async def moderator(self, ctx, mod, subreddit):
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/r/{subreddit}/about/moderators.json") as r:
                    resp = await r.json()
                await cs.close()
                if r.status != 200:
                    return await ctx.send(f"Whoops, something went wrong, Error Code: {r.status}")
                data = resp['data']
                mods = [i for i in data['children'] if str(i['name']).lower() == str(mod).lower()]
                timestamp = [i['date'] for i in mods]
                perms = [p['mod_permissions'] for p in mods]
                if not [i['author_flair_text'] for i in mods][0]:
                    char = "\u200b"
                else:
                    char = f" | {__import__('html').unescape([i['author_flair_text'] for i in mods][0])}"
                this = [f"{i['name']}{char}" for i in mods]
                embed = discord.Embed(colour=self.bot.colour,
                                      description=f"Permissions: {f', '.join(f'**{p.capitalize()}**' for p in perms[0])}\nAdded as Mod: **{datetime.datetime.utcfromtimestamp(timestamp[0]).strftime('%B %d, %Y')}**").set_author(
                    name=this[0])
                embed.set_footer(text=f"r/{subreddit}")
                await ctx.send(embed=embed)

    @commands.command(aliases=['showerthought'], help="hmm :thinking:")
    async def thonk(self, ctx):
        posts = []
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/r/ShowerThoughts/hot.json") as r:
                    res = await r.json()
                await cs.close()
                for i in res['data']['children']:
                    posts.append(i['data'])
                s = random.choice([p for p in posts if not p['stickied']])
                embed = discord.Embed(title=str(s['title']), colour=self.bot.colour,
                                      url=f"https://reddit.com/{s['permalink']}",
                                      description=f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**")
                embed.set_author(name=s['author'])
                embed.set_footer(text=f"{s['upvote_ratio'] * 100:,}% upvote ratio | posted to r/{s['subreddit']}")
                return await ctx.send(embed=embed) if not s['over_18'] or s[
                    'over_18'] and ctx.channel.is_nsfw() else await ctx.send(
                    f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")

    # mod stats

    @commands.command(aliases=['ms'])
    async def modstats(self, ctx, user):
        """Shows you the moderated subreddits of a specific user."""
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/user/{user}/moderated_subreddits/.json") as r:
                    res = await r.json()
                await cs.close()
                if r.status != 200:
                    return await ctx.send("Whoops, something went wrong. Error Code: {}".format(r.status))
                subreddits = res['data']
                reddits = [
                    f"[{subreddit['sr_display_name_prefixed']}](https://reddit.com{subreddit['url']}) • <:member:731190477927219231> **{subreddit['subscribers']:,}**"
                    for subreddit in subreddits]
                numbas = [s['subscribers'] for s in subreddits]
                msg = "Top 15 Subreddits" if len(reddits) > 15 else "Moderated Subreddits"
                modstats = [f"{i}. {v}" for i, v in enumerate(reddits, 1)]
                final_ms = "\n".join(modstats[:15])
                zero_subs = len([item for item in numbas if item == 0])
                one_subs = len([item for item in numbas if item == 1])
                hundred_subs = len([item for item in numbas if item >= 100])
                thousand_subs = len([item for item in numbas if item >= 1000])
                hundred_thousand_subs = len([item for item in numbas if item >= 100_000])
                million = len([item for item in numbas if item >= 1_000_000])
                ten_million = len([item for item in numbas if item >= 10_000_000])
                embed = discord.Embed(
                    description=f"u/{user} mods **{len(reddits):,}** subreddits with **{sum(numbas)}** total readers\n\n*{msg}*\n\n{final_ms}",
                    colour=self.bot.colour)
                embed.add_field(name="Advanced Statistics",
                                value=f"Subreddits with 0 subscribers: **{zero_subs}**\nSubreddits with 1 subscriber: **{one_subs}**\nSubreddits with 100 or more subscribers: **{hundred_subs}**\nSubreddits with 1,000 or more subscribers: **{thousand_subs}**\nSubreddits with 100,000 or more subscribers: **{hundred_thousand_subs}**\nSubreddits with 1,000,000 or more subscribers: **{million}**\nSubreddits with 10,000,000 or more subscribers: **{ten_million}**\n\nAverage Subscribers Per Subreddit: **{humanize.intcomma(round(sum(numbas) / len(numbas)))}**")
            await ctx.send(embed=embed)

    @commands.command(help="Gets a post from a subreddit of your choosing.")
    async def post(self, ctx, subreddit, sort='hot'):
        posts = []
        sorts = ['new', 'hot', 'top', 'rising', 'controversial']
        u = '\u200b'
        if sort not in sorts:
            return await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, that isn't a valid sort! Valid sorts include {', '.join(sorts)}.")
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/r/{subreddit}/{sort}.json") as r:
                    res = await r.json()
                await cs.close()
                for i in res['data']['children']:
                    posts.append(i['data'])
                s = random.choice([p for p in posts if not p['stickied']])
                embed = discord.Embed(title=str(s['title']), colour=self.bot.colour,
                                      url=f"https://reddit.com/{s['permalink']}")
                embed.set_author(name=s['author'])
                embed.set_footer(text=f"{s['upvote_ratio'] * 100:,}% upvote ratio | posted to r/{s['subreddit']}")
                if s['is_self']:
                    embed.description = f"{s['selftext'].replace('**', f'{u}')}\n{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**"
                    return await ctx.send(embed=embed) if not s['over_18'] or s[
                        'over_18'] and ctx.channel.is_nsfw() else await ctx.send(
                        f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
                else:
                    embed.set_image(url=s['url'])
                    embed.description = f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**"
                    return await ctx.send(embed=embed) if not s['over_18'] or s[
                        'over_18'] and ctx.channel.is_nsfw() else await ctx.send(
                        f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")

    @commands.command(help="Shows info about a subreddit")
    async def subreddit(self, ctx, subreddit):
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://reddit.com/r/{subreddit}/about/.json") as r:
                    res = await r.json()
                await cs.close()
                data = res['data']
                icon = data['community_icon'].split("?")[0]
                banner = data['banner_background_image'].split("?")[0]
                embed = discord.Embed(
                    description=f"{data['public_description']}\n**{data['subscribers']:,}** subscribers | **{data['active_user_count']:,}** active users",
                    colour=self.bot.colour).set_author(name=data['display_name_prefixed'],
                                                       url=f"https://reddit.com/r/{subreddit}", icon_url=icon)
                embed.description += f'\n<:asset:734531316741046283> [Icon URL]({str(icon)}) | [Banner URL]({str(banner)})'
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://www.reddit.com/r/{subreddit}/about/moderators.json") as r:
                        resp = await r.json()
                    daba = resp['data']
                    mods = [i for i in daba['children']]
                    embed.add_field(name=f"Mods (Total {len(mods)})", value="\n".join(
                        [f"[{mod['name']}](https://reddit.com/user/{mod['name']})" for mod in mods[:10]]))
                    embed.set_footer(
                        text=f"Subreddit created {humanize.naturaltime(datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(data['created_utc']))}")
                    return await ctx.send(embed=embed) if not data['over18'] or data[
                        'over18'] and ctx.channel.is_nsfw() else await ctx.send(
                        f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")

    @commands.command(aliases=['pages', 'paginate'])
    async def reddit_pages(self, ctx, subreddit, limit: int = 5):
        """Gives you a paginated menu of any subreddit"""
        posts = []
        u = '\u200b'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/{subreddit}/hot.json", params={'limit': 100}) as r:
                res = await r.json()
            await cs.close()
            for i in res['data']['children']:
                posts.append(i['data'])
            counter = 0
            embeds = []
            async with ctx.typing():
                for s in random.sample(posts, len(posts)):
                    embed = discord.Embed(title=str(s['title']), colour=self.bot.colour,
                                          url=f"https://reddit.com/{s['permalink']}")
                    embed.set_author(name=s['author'])
                    embed.set_footer(text=f"{s['upvote_ratio'] * 100:,}% upvote ratio | posted to r/{s['subreddit']}")
                    if s['is_self']:
                        embed.description = f"{s['selftext'].replace('**', f'{u}')}\n{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**"
                    else:
                        embed.set_image(url=s['url'].split("?")[0])
                        embed.description = f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**"
                    embeds.append(embed)
                    counter += 1
                    if counter == limit:
                        break
                    else:
                        continue
        p = paginator.CatchAllMenu(paginator.EmbedSource(embeds))
        p.add_info_fields({self.up: "How many upvotes the post has", "💬": "How many comments the post has",
                           self.share: "How many shares/cross-posts the post has",
                           ":medal:": "How many awards the post has"})
        await p.start(ctx)


def setup(bot):
    bot.add_cog(Reddit(bot))
