import json
import traceback

import async_cleverbot
import discord
import humanize
from discord.ext import commands

from CyberTron5000.utils.cyberformat import minimalize as m, hyper_replace as hr


def secrets():
    with open("json_files/secrets.json", "r") as f:
        return json.load(f)


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.x_r = ":warning:727013811571261540"
        self.bot = async_cleverbot.Cleverbot(secrets()['cleverbot'])
        self.bot.set_context(async_cleverbot.DictContext(self.bot))
        self.channel = self.client.get_channel(self.client.logging['logging_channel'])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Traceback code used from Daggy1234's Dagbot GitHub Repository provided by the GNU Affero General Public License v3.0
        # https://github.com/Daggy1234/dagbot/blob/master/dagbot/extensions/errors.py#L38-L42
        # Copyright (C) 2020  Daggy1234
        et = type(error)
        tb = error.__traceback__
        v = 4
        lines = traceback.format_exception(et, error, tb, v)
        traceback_text = "".join(lines)
        known_errors = [commands.BadArgument, commands.MissingRequiredArgument, commands.MissingPermissions,
                        commands.BotMissingPermissions, commands.CommandOnCooldown, commands.NSFWChannelRequired]
        pass_errors = [commands.NotOwner, commands.CommandNotFound, commands.CheckFailure, commands.BadUnionArgument]
        if type(error) in pass_errors:
            return
        elif type(error) in known_errors:
            await ctx.message.add_reaction(self.x_r)
            await ctx.send(f'<{self.x_r}> **{ctx.author.name}**, {m(str(error))}')
        else:
            embed = discord.Embed(colour=self.client.colour, title="Unkown Error Occured!",
                                  description=f"Error on `{ctx.command}`: `{error.__class__.__name__}`\n```py\n{traceback_text}```\n**Server:** {ctx.guild}\n**Author:** {ctx.author}\n[URL]({ctx.message.jump_url})")
            await ctx.message.add_reaction(self.x_r)
            await self.channel.send(embed=embed)
            await ctx.send(content="The error has been sent to my creator! It will be fixed as soon as possible!",
                           embed=embed)

    @commands.Cog.listener(name="on_message")
    async def on_user_mention(self, message):
        owner = self.client.get_user(350349365937700864) or await self.client.fetch_user(350349365937700864)
        if message.content in ("<@!697678160577429584>", "<@697678160577429584>"):
            DEFAULT_PREFIX = ["c$"]
            a = self.client.prefixes.get(message.guild.id, DEFAULT_PREFIX)
            embed = discord.Embed(colour=self.client.colour,
                                  description=f'**My prefixes for {message.guild} are** {f"{self.client.user.mention}, " + ", ".join([f"`{a}`" for a in a])}\n\n**Do** '
                                              f'{f"{self.client.user.mention} help, " + ", ".join([f"`{a}help`" for a in a])} **for a full list of commands**\n\n→ [Invite](https://cybertron-5k.netlify.app/invite) | [Support](https://cybertron-5k.netlify.app/server) | <:github:724036339426787380> [GitHub](https://github.com/niztg/CyberTron5000) | <:cursor_default:734657467132411914>[Website](https://cybertron-5k.netlify.app) | <:karma:704158558547214426> [Reddit](https://reddit.com/r/CyberTron5000)')
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_author(name=f"Developed by {owner}", icon_url=owner.avatar_url)
            await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        ml = "\n".join([f"{member.mention} • `{member.top_role.name}`" for member in guild.members if
                        member.guild_permissions.administrator and not member.bot])
        botno = len([member for member in guild.members if member.bot])
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        categories = guild.categories
        emojis = guild.emojis
        await self.client.pg_con.execute("INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)", guild.id, "c$")
        try:
            self.client.prefixes[guild.id] = ["c$"]
        except BaseException:
            pass
        embed = discord.Embed(colour=0x00ff00, title=f'{guild}',
                              description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}\n**Owner:** {guild.owner.mention}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**\n{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(
            text=f"Guild created" f"{humanize.naturaltime(__import__('datetime').datetime.utcnow() - guild.created_at)}")
        await guild.me.edit(nick=f"(c$) {self.client.user.name}")
        channels = sorted([t for t in guild.text_channels if t.permissions_for(guild.me).send_messages],
                          key=lambda x: x.position)
        c = [channel for channel in guild.text_channels if guild.me.permissions_in(channel).view_audit_log]
        if not c:
            pass
        else:
            async for action in guild.audit_logs(limit=10):
                if action.action == discord.AuditLogAction.bot_add and action.target == self.client.user:
                    embed.add_field(name="Added By", value=action.user)
                    break
                else:
                    continue
        await channels[0].send(embed=discord.Embed(color=self.client.colour,
                                                   description="Hi, thanks for inviting me! My default prefix is `c$`, but you can change it by doing `c$changeprefix <new prefix>`.\n→ [Invite](https://cybertron-5k.netlify.app/invite) | [Support](https://cybertron-5k.netlify.app/server) | <:github:724036339426787380> [GitHub](https://github.com/niztg/CyberTron5000) | <:cursor_default:734657467132411914>[Website](https://cybertron-5k.netlify.app) | <:karma:704158558547214426> [Reddit](https://reddit.com/r/CyberTron5000)\n"))
        await self.channel.send(f"Joined Guild! This is guild **#{len(self.client.guilds)}**", embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        ml = "\n".join([f"{member.mention} • `{member.top_role.name}`" for member
                        in guild.members if member.guild_permissions.administrator and not member.bot])
        botno = len([member for member in guild.members if member.bot])
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        categories = guild.categories
        emojis = guild.emojis
        await self.client.pg_con.execute("DELETE FROM prefixes WHERE guild_id = $1", guild.id)
        try:
            self.client.prefixes.pop(guild.id)
        except BaseException:
            pass
        embed = discord.Embed(colour=discord.Colour.red(), title=f'{guild}',
                              description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}**\n**Owner:** {guild.owner.mention}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(
            text=f"Guild created {humanize.naturaltime(__import__('datetime').datetime.utcnow() - guild.created_at)}")
        await self.channel.send(f"Left guild. We're down to **{len(self.client.guilds)}** guilds", embed=embed)

    @commands.Cog.listener(name="on_message")
    async def cleverbot_session(self, message):
        if (message.channel.id == 730486269468999741) or (message.channel.id == 730570845013147708):
            if message.author.bot:
                return
            async with message.channel.typing():
                if len(message.content) < 2 or len(message.content) > 100:
                    return await message.channel.send(
                        f"**{message.author.name}**, text must be below 100 characters and over 2.")
                resp = await self.bot.ask(message.content, message.author.id)
                r = str(resp) if str(resp).startswith("I") else m(str(resp))
                if str(r)[-1] not in ['.', '?', '!']:
                    suff = "?" if any(s in str(r) for s in ['who', 'what', 'when', 'where', 'why', 'how']) else "."
                else:
                    suff = "\u200b"
                send = hr(str(r), old=[' i ', "i'm", "i'll"], new=[' I ', "I'm", "I'll"])
                await message.channel.send(f"**{message.author.name}**, {send}{suff}")

    @commands.Cog.listener(name='on_message')
    async def monke(self, message):
        if (message.channel.id == 735694049700347954) or (message.channel.id == 735690974340317216):
            for i in ['🇲', '🇴', '🇳', '🇰', '🇪']:
                await message.add_reaction(i)


def setup(client):
    client.add_cog(Events(client))
