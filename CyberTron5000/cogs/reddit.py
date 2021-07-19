import datetime
import random

import discord
import humanize
from discord.ext import commands
from tabulate import tabulate

from CyberTron5000.utils import paginator
from CyberTron5000.utils.lists import REDDIT_EMOJIS


class Reddit(commands.Cog):
    """Commands interacting with the Reddit API."""

    def __init__(self, bot):
        self.bot = bot
        self.up = "<:upvote:718895913342337036>"
        self.share = "<:share:730823872265584680>"

    # noinspection PyBroadException

    async def cakeday(self, data: dict) -> bool:
        created = datetime.datetime.utcfromtimestamp(data['data']['created_utc'])
        today = datetime.datetime.utcnow()
        return (created.month, created.day) == (today.month, today.day)

    async def get_redditor_data(self, user, option):
        assert option in ("moderated_subreddits", "about", "trophies")
        async with self.bot.session.get(f"https://www.reddit.com/user/{user}/{option}/.json") as r:
            data = await r.json()
        return data

    async def get_post_data(self, subreddit, sort):
        async with self.bot.session.get(f"https://www.reddit.com/r/{subreddit}/{sort}.json", params={'limit': 100}) as r:
            data = await r.json()
        posts = list()
        for item in data['data']['children']:
            posts.append(item['data'])
        return [post for post in posts if not post['stickied']]

    @commands.command(help="Shows your Reddit Stats.", aliases=['rs', 'karma', 'redditor'])
    async def redditstats(self, ctx, redditor):
        troph_list, final = [], []
        try:
            async with ctx.typing():
                user, trophies = await self.get_redditor_data(redditor, 'about'), await self.get_redditor_data(redditor, 'trophies')
                for item in trophies['data']['trophies']:
                    try:
                        troph_list.append(REDDIT_EMOJIS[item['data']['name']])
                    except KeyError:
                        print(f"{item['data']['name']} not in trophies list!")
                for i in troph_list:
                    if i not in final:
                        final.append(i)
                cake = " <:cakeday:736660679938932876>" if await self.cakeday(user) else ''
                icon = user['data']['icon_img']
                icon = icon.split("?")[0]
                banner = user['data']['subreddit']['banner_img']
                banner = banner.split("?")[0]
                embed = discord.Embed(color=self.bot.colour)
                embed.set_thumbnail(url=icon)
                embed.url = f"https://reddit.com/user/{redditor}"
                embed.set_author(name=f"{user['data']['subreddit']['title']}", url=f"https://reddit.com/user/{redditor}") if f"{user['data']['subreddit']['title']}" else None
                embed.title = user['data']['name'] + cake
                embed.description = user['data']['subreddit']['public_description'] + '\n'
                embed.description += f"<:karma:704158558547214426> **{user['data']['link_karma'] + user['data']['comment_karma']:,}** | 🔗 **{user['data']['link_karma']:,}** 💬 **{user['data']['comment_karma']:,}**"
                embed.description += f"\n<:asset:734531316741046283> [Icon URL]({icon})"
                if banner:
                    embed.description += f" [Banner URL]({banner})"
                embed.description += "\n" + ' '.join(final)
                dt = datetime.datetime.utcfromtimestamp(user['data']['created_utc'])
                created = humanize.naturaltime(datetime.datetime.utcnow() - dt)
                embed.add_field(name="Account Settings",
                                value=(f'{ctx.on_off(user["data"]["verified"])} **Verified**\n'
                                       f'{ctx.on_off(user["data"]["is_mod"])} **Is Mod**\n'
                                       f'{ctx.on_off(user["data"]["hide_from_robots"])} **Hide From Robots**\n'
                                       f'{ctx.on_off(user["data"]["has_subscribed"])} **Has Subscribed**')
                                )
                embed.set_footer(text=f'Account created {created}')
            await ctx.send(embed=embed)
        except KeyError:
            raise commands.BadArgument(f'redditor **{redditor}** not found.')

    @commands.command(aliases=['m'], help="Shows you a meme from some of reddit's dankest places (and r/memes)")
    async def meme(self, ctx):
        subreddit = random.choice(['memes', 'meme', 'dankmemes', 'okbuddyretard', 'memeeconomy', 'dankexchange', 'pewdiepiesubmissions', 'wholesomememes'])
        async with ctx.typing():
            s = random.choice(await self.get_post_data(subreddit, 'hot'))
            embed = discord.Embed(title=str(s['title']),
                                  colour=self.bot.colour,
                                  url=f"https://reddit.com/{s['permalink']}",
                                  description=f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**")
            embed.timestamp = datetime.datetime.utcfromtimestamp(s['created'])
            embed.set_author(name=s['author'])
            embed.set_footer(text=f"r/{s['subreddit']} • {s['upvote_ratio'] * 100:,}% upvote ratio")
            embed.set_image(url=s['url'])
        if s['over_18'] and not ctx.channel.is_nsfw():
            raise commands.NSFWChannelRequired(ctx.channel)
        return await ctx.send(embed=embed)

    @commands.command(aliases=['iu'], help="Shows you the banner or icon of a subreddit (on old Reddit).")
    async def icon(self, ctx, subreddit, choice="icon"):
        async with ctx.typing(), self.bot.session.get(f"https://reddit.com/r/{subreddit}/about/.json") as r:
            res = await r.json()
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
        async with ctx.typing(), self.bot.session.get(f"https://www.reddit.com/r/{subreddit}/about/moderators/.json") as r:
            data = await r.json()
            if r.status != 200:
                raise commands.BadArgument(f'subreddit **{subreddit}** not found!')
            mods = data['data']['children']
            try:
                index = [str(m['name']).lower() for m in mods].index(str(mod).lower())
            except ValueError:
                raise commands.BadArgument(f"{mod} doesn't moderate {subreddit}.")
            user = mods[index]
            embed = discord.Embed(colour=self.bot.colour)
            name = f"{user['name']}"
            flair = user['author_flair_text']
            if flair:
                name += f" | {flair}"
            added = datetime.datetime.utcfromtimestamp(user['date'])
            embed.set_author(name=name, icon_url="https://cdn.discordapp.com/emojis/446524953341460491.png?v=1")
            embed.description = "Permissions: " + ", ".join([f"**{perm.title()}**" for perm in user['mod_permissions']])
            embed.description += f"\nAdded as Mod: **{added.strftime('%B %d, %Y')}** ({humanize.naturaltime(datetime.datetime.utcnow()-added)})"
        await ctx.send(embed=embed)

    @commands.command(aliases=['showerthought'], help="hmm :thinking:")
    async def thonk(self, ctx):
        async with ctx.typing():
            s = random.choice(await self.get_post_data('showerthoughts', 'top'))
            embed = discord.Embed(title=str(s['title']),
                                  colour=self.bot.colour,
                                  url=f"https://reddit.com/{s['permalink']}",
                                  description=f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**")
            embed.timestamp = datetime.datetime.utcfromtimestamp(s['created'])
            embed.set_author(name=s['author'])
            embed.set_footer(text=f"r/{s['subreddit']} • {s['upvote_ratio'] * 100:,}% upvote ratio")
        if s['over_18'] and not ctx.channel.is_nsfw():
            raise commands.NSFWChannelRequired(ctx.channel)
        return await ctx.send(embed=embed)

    # mod stats

    @commands.command(aliases=['ms'])
    async def modstats(self, ctx, user):
        """Shows you the moderated subreddits of a specific user."""
        async with ctx.typing():
            subreddit, user = await self.get_redditor_data(user, 'moderated_subreddits'), await self.get_redditor_data(user, 'about')
            embed = discord.Embed(colour=self.bot.colour)
            sub_numb = 0
            data = subreddit.get('data')
            numb_subs = [s['subscribers'] for s in data]
            if not data:
                raise commands.BadArgument("this user doesn't mod any subreddits!")
            subreddits = sorted(data, key=lambda s: s['subscribers'], reverse=True)
            embed.description = f"<:member:731190477927219231> **Total Subscribers: {sum(numb_subs):,}**\n<:reddit:749433072549625897> **Total Subreddits: {len(data)}**\n\n"
            for subreddit in subreddits:
                sub_numb += 1
                embed.description += f"{sub_numb}. [{subreddit['sr_display_name_prefixed']}](https://reddit.com{subreddit['url']}) <:member:731190477927219231> **{subreddit['subscribers']:,}**\n"
                if sub_numb >= 15:
                    break
            subreddit_stats = {
                '0': len([item for item in numb_subs if item == 0]),
                '1': len([item for item in numb_subs if item == 1]),
                '100': len([item for item in numb_subs if item >= 100]),
                '1,000': len([item for item in numb_subs if item >= 1000]),
                '100,000': len([item for item in numb_subs if item >= 100_000]),
                '1,000,000': len([item for item in numb_subs if item >= 1_000_000]),
                '10,000,000': len([item for item in numb_subs if item >= 10_000_000])
            }
            # i know this ^^ is bad
            headers = ["Subscribers", "Number of Subreddits"]
            table = []
            for key, value in subreddit_stats.items():
                table.append([key.strip(), str(value).strip()])
            icon_url = user['data']['icon_img'].split('?')[0]
            embed.set_author(name=f"{user['data']['name']}", icon_url=icon_url)
            if not ctx.author.is_on_mobile():
                table = tabulate(table, headers, tablefmt="fancy_grid")
                embed.add_field(name="Stats", value=f"```\n{table}\n```")
        await ctx.send(embed=embed)

    @commands.command(help="Gets a post from a subreddit of your choosing.")
    async def post(self, ctx, subreddit, sort='hot'):
        posts = []
        sorts = ['new', 'hot', 'top', 'rising', 'controversial']
        if sort not in sorts:
            raise commands.BadArgument(f"that isn't a valid sort! Valid sorts include {', '.join(sorts)}.")
        async with ctx.typing():
            try:
                s = random.choice(await self.get_post_data(subreddit, sort))
            except IndexError:
                raise commands.BadArgument('subreddit not found!')
            embed = discord.Embed(title=str(s['title']), colour=self.bot.colour, url=f"https://reddit.com/{s['permalink']}")
            embed.set_author(name=s['author'])
            embed.set_footer(text=f"r/{s['subreddit']} • {s['upvote_ratio'] * 100:,}% upvote ratio")
            embed.timestamp = datetime.datetime.utcfromtimestamp(s['created'])
            if s['is_self']:
                embed.description = f"{s['selftext']}\n{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**"
            else:
                embed.set_image(url=s['url'])
                embed.description = f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**"
        if s['over_18'] and not ctx.channel.is_nsfw():
            raise commands.NSFWChannelRequired(ctx.channel)
        return await ctx.send(embed=embed)

    @commands.command(help="Shows info about a subreddit")
    async def subreddit(self, ctx, subreddit):
        try:
            async with ctx.typing(), self.bot.session.get(f"https://reddit.com/r/{subreddit}/about/.json") as r, self.bot.session.get(f"https://www.reddit.com/r/{subreddit}/about/moderators/.json") as r1:
                res = await r.json()
                resp = await r1.json()
                data = res['data']
                icon = data['community_icon'].split("?")[0]
                banner = data['banner_background_image'].split("?")[0]
                embed = discord.Embed(description=f"{data['public_description']}\n**{data['subscribers']:,}** subscribers | **{data['active_user_count']:,}** active users", colour=self.bot.colour)
                embed.title = data['display_name_prefixed']
                embed.url = f"https://reddit.com/r/{subreddit}"
                embed.set_thumbnail(url=icon)
                embed.description += f'\n<:asset:734531316741046283> [Icon URL]({str(icon)}) | [Banner URL]({str(banner)})'
                daba = resp['data']
                mods = [i for i in daba['children']]
                embed.add_field(name=f"Mods (Total {len(mods)})", value="\n".join([f"[{mod['name']}](https://reddit.com/user/{mod['name']})" for mod in mods[:10]]))
                embed.set_footer(text=f"Subreddit created {humanize.naturaltime(datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(data['created_utc']))}")
            if data['over18'] and not ctx.channel.is_nsfw():
                raise commands.NSFWChannelRequired(ctx.channel)
            return await ctx.send(embed=embed)
        except KeyError:
            raise commands.BadArgument(f'subreddit {subreddit} not found.')

    @commands.command(aliases=['pages', 'paginate'])
    async def reddit_pages(self, ctx, subreddit, limit: int = 5):
        """Gives you a paginated menu of any subreddit"""
        posts = []
        u = '\u200b'
        async with self.bot.session.get(f"https://www.reddit.com/r/{subreddit}/hot.json", params={'limit': 100}) as r:
            res = await r.json()
        for i in res['data']['children']:
            if i['data']['over_18'] and not ctx.channel.is_nsfw():
                raise commands.NSFWChannelRequired(ctx.channel)
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
        menu = paginator.CatchAllMenu(paginator.EmbedSource(embeds))
        menu.add_info_fields({self.up: "How many upvotes the post has", "💬": "How many comments the post has", self.share: "How many shares/cross-posts the post has", ":medal:": "How many awards the post has"})
        await menu.start(ctx)


def setup(bot):
    bot.add_cog(Reddit(bot))
