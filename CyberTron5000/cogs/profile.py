import collections
from datetime import datetime as dt
from math import ceil
from typing import Union

import discord
import matplotlib
import matplotlib.pyplot as plt
from discord.ext import commands
from humanize import naturaltime as nt

from CyberTron5000.utils import (
    paginator,
    cyberformat,
    checks
)
from CyberTron5000.utils.lists import (
    REGIONS,
    sl,
    status_mapping,
    badge_mapping
)

matplotlib.use('Agg')


# •
class GuildStats:
    """
    Guild Stats
    """

    def __init__(self, ctx):
        self.context = ctx

    @property
    def num_bot(self):
        return len([m for m in self.context.guild.members if m.bot])

    @property
    def status_counter(self):
        return collections.Counter([m.status for m in self.context.guild.members])

    def guild_graph(self):
        status_counts = self.status_counter
        labels = f'Online ({status_counts[discord.Status.online]:,})', f'Do Not Disturb ({status_counts[discord.Status.dnd]:,})', f'Idle ({status_counts[discord.Status.idle]:,})', f'Offline ({status_counts[discord.Status.offline]:,})'
        sizes = [status_counts[discord.Status.online], status_counts[discord.Status.dnd],
                 status_counts[discord.Status.idle], status_counts[discord.Status.offline]]
        colors = ['#42B581', '#E34544', '#FAA619', '#747F8D']
        explode = (0.0, 0, 0, 0)

        patches, texts = plt.pie(sizes, colors=colors, shadow=False, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.pie(sizes, explode=explode, colors=colors,
                autopct='%1.1f%%', shadow=False, startangle=140)

        plt.axis('equal')
        plt.title(f"Total guild members: {len(self.context.guild.members):,}",
                  bbox={'facecolor': '0.8', 'pad': 5})
        fig = plt.savefig("guild.png", transparent=True)
        plt.close(fig=fig)
        return discord.File("guild.png", filename="guild.png")

    async def check_nitro(self, m: Union[discord.Member, int]):
        if isinstance(m, int):
            m = self.context.bot.get_user(m) or await self.context.bot.fetch_user(m)
        if m.is_avatar_animated() or m in self.context.guild.premium_subscribers:
            return True
        if not isinstance(m, discord.User):
            if m.activity:
                for a in m.activities:
                    if a.type == discord.ActivityType.custom:
                        if a.emoji and a.emoji.is_custom_emoji():
                            return True
        return False


class Profile(commands.Cog):
    """Commands interacting with a user or guild's profile."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["av"], help="Gets the avatar of a user.")
    async def avatar(self, ctx, *, avamember: Union[discord.Member, int] = None):
        if isinstance(avamember, int):
            avamember = self.bot.get_user(avamember) or await self.bot.fetch_user(avamember)
        else:
            avamember = avamember or ctx.author
        embed = discord.Embed(colour=self.bot.colour).set_image(url=avamember.avatar_url_as(static_format='png'))
        embed.add_field(name='Formats',
                        value=f"[WEBP]({avamember.avatar_url_as(format='webp')}) | [PNG]({avamember.avatar_url_as(format='png')}) | [JPG]({avamember.avatar_url_as(format='jpg')})")
        if ".gif" in str(avamember.avatar_url):
            embed.set_field_at(index=0, name='Formats',
                               value=f"[WEBP]({avamember.avatar_url_as(format='webp')}) | [PNG]({avamember.avatar_url_as(format='png')}) | [JPG]({avamember.avatar_url_as(format='jpg')}) | [GIF]({avamember.avatar_url})")
        embed.add_field(name="Sizes",
                        value=f'[128]({avamember.avatar_url_as(static_format="png", size=128)}) | [256]({avamember.avatar_url_as(static_format="png", size=256)}) | [512]({avamember.avatar_url_as(static_format="png", size=512)}) | [1024]({avamember.avatar_url_as(static_format="png", size=1024)}) | [2048]({avamember.avatar_url_as(static_format="png", size=2048)})')
        embed.set_author(name=f"{avamember}")
        return await ctx.send(embed=embed)

    @commands.group(aliases=['si', 'serverinfo', 'gi', 'guild', 'server'], help="Gets the guild's info.",
                    invoke_without_command=True)
    async def guildinfo(self, ctx):
        try:
            g = GuildStats(ctx).status_counter
            n = '\n'
            guild = ctx.guild
            people = [f"<:member:731190477927219231>**{len(ctx.guild.members):,}**",
                      f"{sl[discord.Status.online]}**{g[discord.Status.online]:,}**",
                      f"{sl[discord.Status.idle]}**{g[discord.Status.idle]:,}**",
                      f"{sl[discord.Status.dnd]}**{g[discord.Status.dnd]:,}**",
                      f"{sl[discord.Status.offline]}**{g[discord.Status.offline]:,}**",
                      f"<:streaming:734276396037439628>**{len([m for m in ctx.guild.members if m.activity and m.activity.type == discord.ActivityType.streaming])}**",
                      ]
            text_channels = guild.text_channels
            voice_channels = guild.voice_channels
            categories = guild.categories
            region = REGIONS[f"{str(guild.region)}"]
            banner_url = f" [Banner URL]({ctx.guild.banner_url_as(format='png')})" if ctx.guild.banner_url else "\u200b"
            embed = discord.Embed(colour=self.bot.colour,
                                  description=f"**{guild.id}**\n<:owner:730864906429136907> **{guild.owner}**\n🗺 **{region}**\n<:emoji:734231060069613638> **{len(ctx.guild.emojis)}** <:roles:734232012730138744> **{len(ctx.guild.roles)}**\n<:category:716057680548200468> **{len(categories)}** <:text_channel:703726554018086912>**{len(text_channels)}** <:voice_channel:703726554068418560>**{len(voice_channels)}**\n<:asset:734531316741046283> [Icon URL]({ctx.guild.icon_url_as(static_format='png')}){banner_url}"
                                              f"\n{f'{n}'.join(people)}\n<:bot:703728026512392312> **{GuildStats(ctx).num_bot}**\n<:boost:726151031322443787> **Tier: {guild.premium_tier}**\n{guild.premium_subscription_count} {cyberformat.bar(stat=guild.premium_subscription_count, max=30, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>', show_stat=True)} {30}")
            embed.set_author(name=f"{guild}", icon_url=guild.icon_url)
            embed.set_footer(
                text=f"Guild created {nt(dt.utcnow() - ctx.guild.created_at)}")
            await ctx.send(embed=embed)
        except Exception as er:
            await ctx.send(er)

    @guildinfo.command(aliases=['mods'], invoke_without_command=True)
    async def staff(self, ctx):
        """Shows you the mods of a guild"""
        n = "\n"
        owner = ctx.guild.owner.mention
        members = ctx.guild.members
        admins = [admin for admin in members if admin.guild_permissions.administrator and not admin.bot]
        mods = [mod for mod in members if mod.guild_permissions.kick_members and not mod.bot]
        mod_bots = [bot for bot in members if bot.guild_permissions.kick_members and bot.bot]
        await ctx.send(
            embed=discord.Embed(description=f"<:owner:730864906429136907> **OWNER:** {owner}\n"
                                            f"\n**ADMINS** (Total {len(admins)})\n {f'{n}'.join([f'🛡 {admin.mention} - {admin.top_role.mention}' for admin in admins[:10]])}"
                                            f"\n\n**MODERATORS** (Total {len(mods)})\n {f'{n}'.join([f'🛡 {mod.mention} - {mod.top_role.mention}' for mod in mods[:10]])}"
                                            f"\n\n**MOD BOTS** (Total {len(mod_bots)})\n {f'{n}'.join([f'🛡 {bot.mention} - {bot.top_role.mention}' for bot in mod_bots[:10]])}",
                                colour=self.bot.colour).set_author(name=f"Staff Team for {ctx.guild}",
                                                                   icon_url=ctx.guild.icon_url))

    @guildinfo.command(invoke_without_command=True, aliases=['graph'])
    async def chart(self, ctx):
        """Shows a chart of the guild's activity"""
        guild = GuildStats(ctx)
        try:
            image = await self.bot.loop.run_in_executor(None, guild.guild_graph)
        except:
            raise
        embed = discord.Embed(colour=self.bot.colour, name=f"Status Chart for{ctx.guild}", icon_url=ctx.guild.icon_url)
        embed.set_image(url="attachment://guild.png")
        await ctx.send(embed=embed, file=image)

    @guildinfo.command(aliases=['chan'])
    @checks.bruh()
    async def channels(self, ctx):
        """Shows you the channels of a guild that only mods/admins can see."""
        embed = discord.Embed(colour=self.bot.colour).set_author(icon_url=ctx.guild.icon_url_as(format='png'),
                                                                 name=f"Channels in {ctx.guild}")
        for c in ctx.guild.categories:
            x = []
            for i in c.channels:
                if isinstance(i, discord.TextChannel):
                    if i.is_nsfw():
                        channel = "<:nsfw:730852009032286288>"
                    elif str(i.type) == "news":
                        channel = "<:news:730866149109137520>"
                    else:
                        if i.overwrites_for(ctx.guild.default_role).read_messages is False:
                            channel = "<:text_locked:730929388832686090>"
                        else:
                            channel = "<:text_channel:703726554018086912>"
                    x.append(f"{channel} {i.name}")
                elif isinstance(i, discord.VoiceChannel):
                    if i.overwrites_for(ctx.guild.default_role).read_messages is False:
                        channel = "<:voice_locked:730929346881126582>"
                    else:
                        channel = "<:voice_channel:703726554068418560>"
                    x.append(f"{channel} {i.name}")
                else:
                    pass
            embed.add_field(name=f"<:menu:739570837081817160> {c}", value='\u200b' + "\n".join(x), inline=False)

        y = ctx.guild.text_channels + ctx.guild.voice_channels
        chl = []
        for o in y:
            if not o.category:
                if isinstance(o, discord.TextChannel):
                    if o.is_nsfw():
                        channel = "<:nsfw:730852009032286288>"
                    elif str(o.type) == "news":
                        channel = "<:news:730866149109137520>"
                    else:
                        if o.overwrites_for(ctx.guild.default_role).read_messages is False:
                            channel = "<:text_locked:730929388832686090>"
                        else:
                            channel = "<:text_channel:703726554018086912>"
                    chl.append(f"{channel} {o.name}")
                elif isinstance(o, discord.VoiceChannel):
                    if o.overwrites_for(ctx.guild.default_role).read_messages is False:
                        channel = "<:voice_locked:730929346881126582>"
                    else:
                        channel = "<:voice_channel:703726554068418560>"
                    chl.append(f"{channel} {o.name}")

        embed.description = "\n".join(chl)
        await ctx.send(embed=embed)

    @guildinfo.command(aliases=['def-chan'])
    async def default_channels(self, ctx):
        """Shows you the channels of a guild that everyone can see."""
        embed = discord.Embed(colour=self.bot.colour).set_author(icon_url=ctx.guild.icon_url_as(format='png'),
                                                                 name=f"Channels in {ctx.guild}")
        for c in ctx.guild.categories:
            x = []
            for i in c.channels:
                if isinstance(i, discord.TextChannel):
                    if i.is_nsfw():
                        channel = "<:nsfw:730852009032286288>"
                    elif str(i.type) == "news":
                        channel = "<:news:730866149109137520>"
                    else:
                        if i.overwrites_for(ctx.guild.default_role).read_messages is False:
                            continue
                        else:
                            channel = "<:text_channel:703726554018086912>"
                    x.append(f"{channel} {i.name}")
                elif isinstance(i, discord.VoiceChannel):
                    if i.overwrites_for(ctx.guild.default_role).read_messages is False:
                        continue
                    else:
                        channel = "<:voice_channel:703726554068418560>"
                    x.append(f"{channel} {i.name}")
                else:
                    pass
            if x:
                embed.add_field(name=f"<:menu:739570837081817160> {c}", value='\u200b' + "\n".join(x), inline=False)
            else:
                pass
        y = ctx.guild.text_channels + ctx.guild.voice_channels
        chl = []
        for o in y:
            if not o.category:
                if isinstance(o, discord.TextChannel):
                    if o.is_nsfw():
                        channel = "<:nsfw:730852009032286288>"
                    elif str(o.type) == "news":
                        channel = "<:news:730866149109137520>"
                    else:
                        if o.overwrites_for(ctx.guild.default_role).read_messages is False:
                            continue
                        else:
                            channel = "<:text_channel:703726554018086912>"
                    chl.append(f"{channel} {o.name}")
                elif isinstance(o, discord.VoiceChannel):
                    if o.overwrites_for(ctx.guild.default_role).read_messages is False:
                        continue
                    else:
                        channel = "<:voice_channel:703726554068418560>"
                    chl.append(f"{channel} {o.name}")

        embed.description = "\n".join(chl)
        await ctx.send(embed=embed)
        
    @guildinfo.command(aliases=['role-chan', 'rc'])
    async def role_channels(self, ctx, role: discord.Role):
        """Shows you the channels of a guild that everyone can see."""
        embed = discord.Embed(colour=self.bot.colour).set_author(icon_url=ctx.guild.icon_url_as(format='png'),
                                                                 name=f"Channels in {ctx.guild}")
        for c in ctx.guild.categories:
            x = []
            for i in c.channels:
                if isinstance(i, discord.TextChannel):
                    if i.is_nsfw():
                        channel = "<:nsfw:730852009032286288>"
                    elif str(i.type) == "news":
                        channel = "<:news:730866149109137520>"
                    else:
                        if i.overwrites_for(role).read_messages is False:
                            continue
                        else:
                            channel = "<:text_channel:703726554018086912>"
                    x.append(f"{channel} {i.name}")
                elif isinstance(i, discord.VoiceChannel):
                    if i.overwrites_for(role).read_messages is False:
                        continue
                    else:
                        channel = "<:voice_channel:703726554068418560>"
                    x.append(f"{channel} {i.name}")
                else:
                    pass
            if x:
                embed.add_field(name=f"<:menu:739570837081817160> {c}", value='\u200b' + "\n".join(x), inline=False)
            else:
                pass
        y = ctx.guild.text_channels + ctx.guild.voice_channels
        chl = []
        for o in y:
            if not o.category:
                if isinstance(o, discord.TextChannel):
                    if o.is_nsfw():
                        channel = "<:nsfw:730852009032286288>"
                    elif str(o.type) == "news":
                        channel = "<:news:730866149109137520>"
                    else:
                        if o.overwrites_for(role).read_messages is False:
                            continue
                        else:
                            channel = "<:text_channel:703726554018086912>"
                    chl.append(f"{channel} {o.name}")
                elif isinstance(o, discord.VoiceChannel):
                    if o.overwrites_for(role).read_messages is False:
                        continue
                    else:
                        channel = "<:voice_channel:703726554068418560>"
                    chl.append(f"{channel} {o.name}")

        embed.description = "\n".join(chl)
        await ctx.send(embed=embed)

    @commands.command(help="Gets a user's info.")
    async def betteruserinfo(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=str(member), colour=0xb00b69).set_thumbnail(url=member.avatar_url).set_image(
            url=member.avatar_url)
        embed.add_field(name="roles", value=",".join(r.mention for r in member.roles[::-1][:15]))
        embed.add_field(name='name', value='\u200b')
        embed.add_field(name=member.name, value=member.display_name)
        embed.add_field(name='dates', value=f'made acount: {member.created_at}\njoined server: {member.joined_at}')
        embed.add_field(name=f'status: :{member.status}:', value='\u200b')
        embed.timestamp = ctx.message.created_at
        embed.colour = member.colour
        embed.set_footer(text='created today')
        embed.add_field(name='is a bot?', value=f'{member.bot}')
        embed.add_field(name='bad', value='ges {member.bdages}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['mi', 'member', 'ui', 'user', 'userinfo'])
    async def memberinfo(self, ctx, *, member: Union[discord.Member, int] = None):
        """
        Gives you userinfo
        """
        embed = discord.Embed(color=self.bot.colour)
        if isinstance(member, int):
            m = self.bot.get_user(member) or await self.bot.fetch_user(member)
        else:
            m = member or ctx.author
        embed.set_author(name=str(m), icon_url=m.avatar_url, url=m.avatar_url_as(static_format='png', size=4096))
        if not m.bot:
            is_bot = ""
        else:
            if m.public_flags.verified_bot:
                is_bot = "<:verifiedbot1:730904128397639682><:verifiedbot2:730904163365421128>"
            else:
                is_bot = "<:bot:703728026512392312>"
        mem_flags = dict(m.public_flags).items()
        final = [k for k, v in mem_flags if v]
        a = [badge_mapping[str(b)] for b in final if b in badge_mapping]
        a.append("<:nitro:730892254092198019>") if await GuildStats(ctx).check_nitro(m) else None
        if isinstance(m, discord.User):
            embed.description = f'{is_bot} {" ".join(a)}\n→ ID **{m.id}**\n'
            embed.description += f'→ Created Account **{nt(dt.utcnow() - m.created_at)}**\n'
            embed.description += f'→ Guilds Shared With Bot **{len([g for g in ctx.bot.guilds if g.get_member(m.id)])}**'
            embed.description += f'\n→ [Avatar URL]({m.avatar_url_as(static_format="png", size=4096)})\n'
            return await ctx.send(embed=embed)
        elif isinstance(m, discord.Member):
            local_emojis = []
            if m == ctx.guild.owner:
                local_emojis.append("<:owner:730864906429136907>")
            if m.permissions_in(ctx.channel).ban_members:
                local_emojis.append("<:ban:735959654504333407>")
            if m in ctx.guild.premium_subscribers:
                local_emojis.append("<:nitro:731722710283190332>")
            char = '\u200b' if not a or not local_emojis else " "
            n = f' | {m.display_name}' if m.name != m.display_name else ""
            embed.set_author(name=str(m) + n, icon_url=m.avatar_url,
                             url=m.avatar_url_as(static_format='png', size=4096))
            le = " ".join(local_emojis)
            if not a and not local_emojis and is_bot == '':
                embed.description = f'\n→ ID **{m.id}**\n'
            else:
                embed.description = f'{is_bot}{" ".join(a)}{char}{le}\n→ ID **{m.id}**\n'
            embed.description += f'→ Created Account **{nt(dt.utcnow() - m.created_at)}**\n'
            embed.description += f'→ Joined Guild **{nt(dt.utcnow() - m.joined_at)}**\n'
            embed.description += f'→ Guilds Shared With Bot **{len([g for g in ctx.bot.guilds if g.get_member(m.id)])}**'
            if m.top_role.id == ctx.guild.id:
                pass
            else:
                embed.description += f'\n→ Roles **{len([r for r in m.roles if r.id != ctx.guild.id])}** | Top Role {m.top_role.mention}'
            embed.description += f'\n→ [Avatar URL]({m.avatar_url_as(static_format="png", size=4096)})\n'
            embed.add_field(name='Status',
                            value=f'{sl[m.web_status]} **Web Status**\n{sl[m.desktop_status]} **Desktop Status**\n{sl[m.mobile_status]} **Mobile Status**')
            if m.status == discord.Status.offline or not m.activities:
                pass
            else:
                activities = []
                for activity in m.activities:
                    if isinstance(activity, discord.Spotify):
                        activity = f'Listening to **{activity.title}** by **{", ".join(activity.artists)}**'
                    elif isinstance(activity, discord.Game):
                        activity = f'Playing **{activity.name}**'
                    elif isinstance(activity, discord.Streaming):
                        activity = f'Streaming **{activity.name}** on **{activity.platform}**'
                    else:
                        emoji = ''
                        if activity.emoji:
                            emoji = '<:emoji:734231060069613638>' if activity.emoji.is_custom_emoji() and not ctx.bot.get_emoji(
                                activity.emoji.id) else activity.emoji
                        char = "\u200b" if activity.type == discord.ActivityType.custom else " "
                        if str(activity.name) == "None":
                            ac = "\u200b"
                        else:
                            ac = str(activity.name)
                        activity = f'{emoji} {status_mapping[activity.type]}{char}**{ac}**'
                    activities.append(activity)
                embed.add_field(name='Activities', value='\n'.join(activities))
        return await ctx.send(embed=embed)

    @commands.command(aliases=['perms'], help="Gets a user's permissions in the current channel.")
    async def permissions(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        all_perms = list()
        embed = discord.Embed(colour=self.bot.colour).set_author(name=f"{member}'s permissions in {ctx.channel}",
                                                                 icon_url=member.avatar_url)
        all = dict(member.permissions_in(ctx.channel)).items()
        for key, value in all:
            all_perms.append((f"{ctx.tick(value)} **{key.title().replace('_', ' ')}**", value))
        perms = sorted(all_perms, key=lambda x: x[1], reverse=True)
        source = paginator.IndexedListSource(data=[perm[0] for perm in perms], show_index=False, title="Permissions",
                                             per_page=16, embed=embed)
        await paginator.CatchAllMenu(source=source).start(ctx)

    @commands.command(aliases=['ri'])
    async def roleinfo(self, ctx, *, role: discord.Role):
        """Gives you roleinfo"""
        embed = discord.Embed(colour=role.colour).set_author(name=f"{role.name} | {role.id}")
        embed.description = f"{ctx.tick(role.hoist)} **Hoisted**\n"
        embed.description += f"{ctx.tick(role.managed)} **Managed**\n"
        embed.description += f"{ctx.tick(role.mentionable)} **Mentionable**\n"
        permissions = dict(role.permissions).items()
        perms = []
        for k, v in permissions:
            if v:
                perms.append(f"{str(k.title()).replace('_', ' ')}")
        embed.add_field(name='Permissions', value='**\u200b' + ', '.join(perms) + '**')
        embed.description += f"\n:paintbrush: **{role.colour}**\n<:member:731190477927219231> **{len(role.members)}**\n<:ping:733142612839628830> {role.mention}"
        embed.set_footer(text=f'Role created {nt(dt.utcnow() - role.created_at)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['spot'])
    async def spotify(self, ctx, *, member: discord.Member = None):
        """Shows a member's spotify status"""
        member = member or ctx.author
        spotify = discord.utils.get(member.activities, type=discord.ActivityType.listening)
        if not spotify:
            return await ctx.send(f"{member} is not listening to Spotify!")
        embed = discord.Embed(colour=spotify.colour)
        le_bar = cyberformat.bar(stat=(dt.utcnow() - spotify.start).seconds, max=spotify.duration.seconds,
                                 filled='<:full:739980860371107899>', empty='<:empty:739980654019870720>',
                                 show_stat=True)
        embed.set_thumbnail(url=spotify.album_cover_url)
        embed.description = f"[{spotify.title}](https://open.spotify.com/track/{spotify.track_id})\n"
        embed.description += f"by {spotify.artist}\n"
        embed.description += f"on {spotify.album}\n"
        embed.description += f"{dt.utcfromtimestamp((dt.utcnow() - spotify.start).seconds).strftime('%-M:%S')} {le_bar} {dt.utcfromtimestamp(spotify.duration.seconds).strftime('%-M:%S')}"
        embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/739983277053706302.png?v=1', text=str(member))
        await ctx.send(embed=embed)

    @guildinfo.command()
    async def roles(self, ctx):
        """A paginated menu of all of the guild's roles."""
        roles = sorted(ctx.guild.roles, key=lambda r: r.position, reverse=True)
        source = paginator.IndexedListSource(data=["{0.mention} <:member:731190477927219231> **{1}**".format(r, len(r.members)) for r in roles], embed=discord.Embed(colour=self.bot.colour))
        await paginator.CatchAllMenu(source=source).start(ctx)

    @commands.command(aliases=['channel', 'chan', 'ci'])
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        """Shows info on a channel."""
        async with ctx.typing():
            channel = channel or ctx.channel
            td = {
                True: "<:nsfw:730852009032286288>",
                False: "<:text_channel:703726554018086912>",
            }
            if channel.overwrites_for(ctx.guild.default_role).read_messages is False:
                url = "<:text_locked:730929388832686090>"
            else:
                if channel.is_news():
                    url = "<:news:730866149109137520>"
                else:
                    url = td[channel.is_nsfw()]
            embed = discord.Embed(colour=self.bot.colour)
            embed.title = f"{url} {channel.name} | {channel.id}"
            last_message = await channel.fetch_message(channel.last_message_id)
            pins = await channel.pins()
            embed.description = (
                                 f"{channel.topic or ''}\n{f'<:category:716057680548200468> **{channel.category}**' if channel.category else ''} "
                                 f"<:member:731190477927219231> **{len(channel.members):,}** "
                                 f"{f'<:pin:735989723591344208> **{len(pins)}**' if pins else ''} <:msg:735993207317594215> [Last Message]({last_message.jump_url})"
                                )
            embed.description = f"{channel.topic or ''}\n{f'<:category:716057680548200468> **{channel.category}**' if channel.category else ''} <:member:731190477927219231> **{len(channel.members):,}** {f'<:pin:735989723591344208> **{len([*await channel.pins()])}**' if await channel.pins() else ''} <:msg:735993207317594215> [Last Message]({last_message.jump_url})"
            embed.set_footer(
                text=f'Channel created {nt(dt.utcnow() - channel.created_at)}')
        await ctx.send(embed=embed)

    def emote_pages(self, ctx: commands.Context, amount: int):
        messages = ['']
        messages *= ceil(
            len(ctx.guild.emojis) / amount)  # now the list has all the messages we need to send, they're just empty.
        for i in range(len(messages)):
            start = i * amount
            end = amount * (i + 1)
            # now we have the ranges for each message. we will edit each item in the list and then send them.
            for emoji in ctx.guild.emojis[start:end]:
                # formatting the items in the list
                messages[i] += "{0} • `{0}`\n".format(emoji.__str__())
        if any([item for item in messages if len(item) > 1999]):
            raise ValueError("The amount you chose was too large. Try again with a smaller amount.")
        return messages

    @commands.command(aliases=['elf'])
    async def emote_list_formatter(self, ctx, amount: int = 20):
        """Get a layout of emojis for your guild."""
        try:
            messages = self.emote_pages(ctx, amount)
        except ValueError as error:
            raise commands.BadArgument(str(error))
        for message in messages:
            await ctx.send(message)

    @guildinfo.command(aliases=['em'])
    async def emojis(self, ctx):
        """A paginated menu of all of the guild's emojis."""
        embeds = []
        for page in self.emote_pages(ctx, 20):
            embeds.append(discord.Embed(colour=self.bot.colour, description=page))
        await paginator.CatchAllMenu(source=paginator.EmbedSource(embeds)).start(ctx)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadUnionArgument):
            return await ctx.send("That member or user was not found!")


def setup(bot):
    bot.add_cog(Profile(bot))