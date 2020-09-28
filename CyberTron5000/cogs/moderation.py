import asyncio
from typing import Union
from datetime import datetime as dt

import discord
import json
import humanize
from discord.ext import commands, flags

from CyberTron5000.utils import paginator, lists, cyberformat, checks
from CyberTron5000.utils.models.infractions import *
from CyberTron5000.utils.converter import Prefix


def ct5k():
    def predicate(ctx):
        return ctx.guild.id == 715743556488396872
    return commands.check(predicate)

# ≫


class Moderation(commands.Cog):
    """Commands for Moderation"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.guild is not None

    def hierarchy(self, member):
        # check if I can action this user
        return member.guild.me.top_role > member.top_role and member != member.guild.owner

    @flags.add_flag("--user", type=discord.User)
    @flags.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int, **flags):
        """Purges a given amount of messages."""
        amount += 1
        await ctx.message.delete()
        user = flags.get('user')
        if user:
            await ctx.channel.purge(limit=amount, check=lambda msg: msg.author == user)
            return await ctx.send(f'{ctx.tick()} **{amount - 1}** messages by {user} have been purged', delete_after=3)
        await ctx.channel.purge(limit=amount)
        return await ctx.send(f"{ctx.tick()} **{amount - 1}** messages have been purged", delete_after=3)

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from a guild."""
        if not self.hierarchy(member):
            return await ctx.send('I cannot moderate that user')
        r = reason or "No reason specified"
        await member.kick(reason=r)
        try:
            await member.send(
                f"Hello, you have been kicked from participating in {ctx.guild}. Please see your reason for removal: `{r}`")
        except:
            pass
        await ctx.message.add_reaction(ctx.tick())

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: Union[discord.Member, int], *, reason=None):
        """Ban a user from the guild."""
        if isinstance(user, int):
            try:
                user = self.bot.get_user(user) or await self.bot.fetch_user(user)
            except:
                return await ctx.send("This user does not exist!")
        else:
            if not self.hierarchy(user):
                return await ctx.send("I can't moderate that user.")
            user = user
        reason = reason or "No reason provided."
        await ctx.guild.ban(user=user, reason=reason, delete_message_days=7)
        await ctx.send(f"{ctx.tick()} {str(user)} banned! Reason:\n> {reason}")

    @commands.command(usage='<user id|user name#user discriminator>')
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, user, *, reason=None):
        """Unban someone from the guild"""
        bans = await ctx.guild.bans()
        reason = reason or "No reason provided."
        if not user.isdigit():
            for ban in bans:
                if str(ban.user) == user:
                    await ctx.guild.unban(user=ban.user, reason=reason)
                    return await ctx.send(f"{ctx.tick()} {str(user)} was unbanned! Reason:\n> {reason}")
            return await ctx.send("That user was not found in this guild's bans!")
        else:
            try:
                user = self.bot.get_user(user) or await self.bot.fetch_user(user)
            except:
                return await ctx.send("That user was not found!")
            if user.id not in [ban.user.id for ban in bans]:
                return await ctx.send(f"{str(user)} is not banned!")
            await ctx.guild.unban(user=user, reason=reason)
            return await ctx.send(f"{ctx.tick()} {str(user)} was unbanned! Reason:\n> {reason}")

    @commands.group(usage='<poll|option1|option2|option3...>', aliases=['poll'], invoke_without_command=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def vote(self, ctx, *, message):
        """Vote on something."""
        options = message.split("|")
        if not 3 <= (len(options)) < 21:
            return await ctx.send(
                f"You must have a minimum of **2** options and a maximum of **20**! Remember to split your question and options with a `|`, e.g. `what is your favourite food?|pizza|cake|fries`")
        question = options[0]
        _options = options[1:]
        if len(question) >= 100:
            return await ctx.send("Your question is too long, please make it less than 100 characters.")
        if any(len(v) > 80 for v in _options):
            return await ctx.send(
                "One of your options is too long. Note that each option must be less than 80 characters.")
        question += "?" if not (question.endswith(('.', '?', '!'))) else '\u200b'
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.title = question
        votes = []
        for x in range(len(_options)):
            emoji = cyberformat.to_emoji(x)
            _vote_dict = {'emoji': str(emoji), 'question': _options[x], 'votes': 0}
            votes.append(_vote_dict)
        _q_format = []
        for item in votes:
            if not item['question']:
                votes.remove(item)
                continue
            _q_format.append(f"{item['emoji']} **{item['question']}** • {cyberformat.bar(0, 10, '■', '□')}")
        embed.description = f"\n".join(_q_format)
        _msg = await ctx.send(embed=embed)
        for a in votes:
            await _msg.add_reaction(a['emoji'])
        gvotes = self.bot.global_votes  # convenience
        gvotes[_msg.id] = {'embed': embed, 'data': votes}
        # the rest of le magic happens in https://github.com/niztg/CyberTron5000/blob/master/CyberTron5000/cogs/events.py/#L159-217

    @vote.command()
    async def quick(self, ctx, *, poll):
        """A quick upvote/downvote poll. Nothing fancy."""
        # if you don't want the good poll command
        # use this
        UPVOTE = self.bot.get_emoji(751314607808839803)
        DOWNVOTE = self.bot.get_emoji(751314712179900457)
        embed = discord.Embed(
            colour=self.bot.colour,
            description=poll
        )
        embed.add_field(name="Vote Now!",
                        value=f"{UPVOTE} **Yes!**\n{DOWNVOTE} **No!**")
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        [await msg.add_reaction(x) for x in (UPVOTE, DOWNVOTE)]

    @commands.command(name='user-nick', help="Change a user's nickname.", aliases=['usernick', 'un'])
    @commands.has_permissions(manage_nicknames=True)
    async def user_nick(self, ctx, member: discord.Member, *, name=None):
        nick = name or member.name
        if not self.hierarchy(member):
            return await ctx.send('I cannot moderate that user')
        await member.edit(nick=nick)
        await ctx.message.add_reaction(emoji=ctx.tick())

    @commands.command()
    @checks.check_mod_or_owner()
    async def leave(self, ctx):
        """Makes bot leave server"""
        await ctx.guild.leave()

    @commands.command(aliases=['audit'])
    @commands.has_permissions(view_audit_log=True)
    @commands.bot_has_guild_permissions(view_audit_log=True)
    async def auditlog(self, ctx, limit: int = 20):
        try:
            actions = []
            async for x in ctx.guild.audit_logs(limit=limit):
                if not x.target:
                    target = ''
                else:
                    target = x.target
                actions.append(
                    f"{x.user.name} {lists.audit_actions[x.action]} {str(target)} ({humanize.naturaltime(__import__('datetime').datetime.utcnow() - x.created_at)})")
            source = paginator.IndexedListSource(embed=discord.Embed(colour=self.bot.colour).set_author(
                name=f"Last Audit Log Actions for {ctx.guild}",
                icon_url="https://cdn.discordapp.com/emojis/446847139977625620.png?v=1"), data=actions)
            menu = paginator.CatchAllMenu(source=source)
            await menu.start(ctx)
        except Exception as er:
            await ctx.send(f'{er.__class__.__name__}, {er}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, time: int = 10):
        time *= 60
        role = discord.utils.get(ctx.guild.roles, name='CyberMute')
        if not role:
            try:
                role = await ctx.guild.create_role(name='CyberMute', reason='mute')
                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages=False,
                                                  read_message_history=False,
                                                  read_messages=False)
                    positions = {
                        role: ctx.guild.me.top_role.position - 1
                    }
                    await ctx.guild.edit_role_positions(positions=positions)
            except discord.Forbidden:
                await ctx.send("I can't mute in this guild! Please give me role privileges to enable this.")
        if role in member.roles:
            return await ctx.send("Member already muted!")
        else:
            await member.add_roles(role)
            await ctx.message.add_reaction(emoji=ctx.tick())
            await asyncio.sleep(time)
            if role in member.roles:
                await ctx.send(f"{member.mention} unmuted automatically.")
                await member.remove_roles(role)
            else:
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, *, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="CyberMute")
        if not role:
            return await ctx.send("No one on this server was muted using me!")
        if role not in member.roles:
            return await ctx.send("This user is not muted!")
        await member.remove_roles(role)
        await ctx.message.add_reaction(emoji=ctx.tick())
        await ctx.send(f"{member.mention} has been unmuted.")

    @commands.group(invoke_without_command=True, aliases=['pre', 'prefix'], name='changeprefix')
    async def _prefix(self, ctx):
        """View the guild's current prefixes."""
        prefixes = self.bot.prefixes.get(ctx.guild.id, ['c$'])
        all_prefixes = ['`@CyberTron5000#1758` 🔒'] + [f'`{pref}`' for pref in prefixes]
        embed = discord.Embed(color=self.bot.colour)
        embed.set_author(name=f"Prefixes for {ctx.guild}", icon_url=ctx.guild.icon_url)
        embed.description = "\n".join([f'{i}. {v}' for i, v in enumerate(all_prefixes, 1)])
        embed.set_footer(text=f"Total {len(all_prefixes)}")
        await ctx.send(embed=embed)

    @_prefix.command()
    @checks.check_mod_or_owner()
    async def add(self, ctx, *, prefix: Prefix):
        """Add a prefix for the guild."""
        prefixes = self.bot.prefixes.get(ctx.guild.id, ["c$"])
        if prefix in prefixes:
            return await ctx.send(f"`{prefix}` is already a prefix for this guild!")
        if len(prefixes) > 15:
            return await ctx.send("This guild already has 15 prefixes! Please remove some before continuing.")
        await self.bot.db.execute("INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)", ctx.guild.id,
                                  prefix)
        try:
            self.bot.prefixes[ctx.guild.id].append(prefix)
        except KeyError:
            self.bot.prefixes[ctx.guild.id] = ["c$", prefix]
        await ctx.send(f'{ctx.tick()} Success! `{prefix}` is now a prefix in {ctx.guild}!')

    @_prefix.command(aliases=['sp-add'])
    @checks.check_mod_or_owner()
    async def spaceprefix_add(self, ctx, *, prefix: Prefix):
        """Add a prefix for the guild that ends in a space."""
        prefixes = self.bot.prefixes.get(ctx.guild.id, ["c$"])
        if prefix in prefixes:
            return await ctx.send(f"`{prefix}` is already a prefix for this guild!")
        if len(prefixes) > 15:
            return await ctx.send("This guild already has 15 prefixes! Please remove some before continuing.")
        await self.bot.db.execute("INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)", ctx.guild.id,
                                  f"{prefix} ")
        try:
            self.bot.prefixes[ctx.guild.id].append(f"{prefix} ")
        except KeyError:
            self.bot.prefixes[ctx.guild.id] = [f"{prefix} ", "c$"]
        await ctx.send(f'{ctx.tick()} Success! `{prefix} ` is now a prefix in {ctx.guild}!')

    @_prefix.command(aliases=['rm'])
    @checks.check_mod_or_owner()
    async def remove(self, ctx, *, prefix: Prefix):
        """Remove a prefix for the guild."""
        prefixes = self.bot.prefixes.get(ctx.guild.id)
        if prefix not in prefixes:
            return await ctx.send(f"`{prefix}` is not a prefix in {ctx.guild}!")
        await self.bot.db.execute("DELETE FROM prefixes WHERE prefix = $1 AND guild_id = $2", prefix,
                                  ctx.guild.id)
        try:
            self.bot.prefixes[ctx.guild.id].remove(prefix)
        except KeyError:
            self.bot.prefixes[ctx.guild.id] = []
        await ctx.send(f'{ctx.tick()} `{prefix}` is no longer a prefix for {ctx.guild}')

    @_prefix.command(aliases=['sp-rm'])
    @checks.check_mod_or_owner()
    async def spaceprefix_remove(self, ctx, *, prefix: Prefix):
        """Remove a prefix for the guild."""
        prefixes = self.bot.prefixes.get(ctx.guild.id)
        if f"{prefix} " not in prefixes:
            return await ctx.send(f"`{prefix} ` is not a prefix in {ctx.guild}!")
        await self.bot.db.execute("DELETE FROM prefixes WHERE prefix = $1 AND guild_id = $2", f"{prefix} ",
                                  ctx.guild.id)
        try:
            self.bot.prefixes[ctx.guild.id].remove(f"{prefix} ")
        except KeyError:
            self.bot.prefixes[ctx.guild.id] = []
        await ctx.send(f'{ctx.tick()} `{prefix} ` is no longer a prefix for {ctx.guild}')

    @add.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"You need the **Kick Members** permission to run this command.")

    @remove.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"You need the **Kick Members** permission to run this command.")

    @commands.command(aliases=["n", "changenickname", "nick"])
    @checks.check_mod_or_owner()
    async def nickname(self, ctx, *, nickname=None):
        """Change the bot's nickname"""
        nickname = nickname or self.bot.user.name
        try:
            await ctx.guild.me.edit(nick=nickname)
            await ctx.message.add_reaction(ctx.tick())
        except:
            return await ctx.send("I can't change my nickname in this guild.")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            return await ctx.send("I don't have the permissions to do that!")

    @commands.group(invoke_without_command=True)
    @checks.mod()
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided."):
        """Warn a user"""
        user = InfractionUser(guild_id=ctx.guild.id, user_id=member.id)
        infraction = user.add_infraction(reason=reason)
        embed = discord.Embed(
            colour=self.bot.colour,
            description=f"""
    {ctx.tick()} {member} has received a warning.
    > {reason}
    **Infraction Number:** {infraction.infraction_number}
    **Valid Infractions:** {user.num_valid_infractions}
    {ctx.tick(infraction.is_null)} **Is Null?**
    """,
            timestamp=infraction.created
        )
        await ctx.send(embed=embed)
        punishments = {
            "mute": self.bot.get_command('mute'),
            "kick": self.bot.get_command('kick'),
            "ban": self.bot.get_command('ban')
        }
        p = user.determine_punishment()
        punishment = punishments.get(p)
        if not punishment:
            return
        await ctx.send(
            f"{ctx.author.mention}, **{member.name}** has recieved their {user.num_valid_infractions} punishment. This makes them eligible for a **{p}**\n**Do you want to carry out this punishment?** [y/n]")
        msg = await self.bot.wait_for('message', timeout=30, check=lambda x: x.author == ctx.author)
        if msg.content.lower().startswith('y'):
            try:
                await ctx.invoke(punishment, member)
            except Exception:
                raise commands.BotMissingPermissions(
                    "I don't have the requisite permissions to do this, or I can't moderate this user! Please give me the permissions to do this.")
        else:
            await ctx.send(
                f"Ok, user not punished. If you ever want to punish them, simply do `{ctx.prefix}{p} {member}`.")

    @warn.command()
    async def list(self, ctx, member: discord.Member = None):
        """List all of the warns of a user"""
        command = self.bot.get_command('infractions')
        await ctx.invoke(command, member)

    @commands.command()
    async def infractions(self, ctx, member: discord.Member = None):
        """List all of the warns of a user"""
        member = member or ctx.author
        user = InfractionUser(ctx.guild.id, member.id)
        embed = discord.Embed(
            colour=self.bot.colour
        )
        for infraction in user:
            embed.add_field(name=f"**Infraction #{infraction.infraction_number}:**",
                            value=f"> {infraction.reason}\nIssued **{humanize.naturaltime(dt.utcnow() - infraction.created)}**\n{ctx.tick(infraction.is_null)} **Is Null?**")
        embed.set_author(name=f"All of {member.display_name}'s warnings", icon_url=member.avatar_url)
        embed.description = f"All Infractions: `{user.num_infractions}`\nValid Infractions: `{user.num_valid_infractions}`\n\n"
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            embed.remove_field(len(embed.fields) - 1)

    @warn.command()
    @checks.mod()
    async def nullify(self, ctx, member: discord.Member, infraction_no: int):
        """Nullify a warning so it doesn't count towards punishments"""
        try:
            infraction = Infraction.by_infraction_no(ctx.guild.id, member.id, infraction_no)
            null = infraction.is_null
            infraction.nullify()
        except Exception as error:
            return await ctx.send(error)
        if null:
            await ctx.send(
                f"{ctx.tick(not null)} Infraction #{infraction.infraction_number} for {member}: `un-nullified`")
        else:
            await ctx.send(
                f"{ctx.tick(not null)} Infraction #{infraction.infraction_number} for {member}: `nullified`")

    @warn.command()
    @checks.mod()
    async def edit(self, ctx, member: discord.Member, number: int, *, reason):
        """Edit the reason for a warn"""
        try:
            infraction = Infraction.by_infraction_no(ctx.guild.id, member.id, number)
            infraction.edit(reason=reason)
        except Exception as error:
            return await ctx.send(error)
        await ctx.send(f"{ctx.tick()} Infraction #{infraction.infraction_number} edited to:\n> {infraction.reason}")

    @flags.add_flag("--mute", type=int)
    @flags.add_flag("--kick", type=int)
    @flags.add_flag("--ban", type=int)
    @flags.group(invoke_without_command=True, aliases=['sgp'])
    @commands.has_permissions(administrator=True)
    async def set_guild_punishments(self, ctx, **flags):
        """Set the guild punishments for a server.\n\nE.g. `sgp --mute 2 --kick 4 --ban 6`"""
        new_dict = {key: value for key, value in flags.items() if value}
        set_infraction_punishments(ctx.guild.id, **new_dict)
        single, double = "'", '"'
        await ctx.send(
            "Infraction Punishments edited to:\n" + f"```json\n{str(new_dict).replace(single, double)}\n```")

    @set_guild_punishments.command()
    @checks.mod()
    async def info(self, ctx):
        """Shows you info on guild punishments"""
        embed = discord.Embed(
            colour=self.bot.colour,
            title=f"Infraction Punishment Info",
            description="\n\n".join(
                [f"**{key}**:\n{value.format(ctx.prefix)}" for key, value in lists.INFRACTION_DESCRIPTIONS.items()])
        )
        await ctx.send(embed=embed)

    @warn.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, member: discord.Member):
        """Clear all of a user's infractions"""
        user = InfractionUser(guild_id=ctx.guild.id, user_id=member.id)
        user.clear_punishments()
        await ctx.message.add_reaction(ctx.tick())

    @commands.command(aliases=['vgp'])
    @checks.mod()
    async def view_guild_punishments(self, ctx):
        """View the guild's punishment levels"""
        data = json.load(open(FILENAME))
        signature = f"`{ctx.prefix}sgp --mute [punishments for mute] --kick [punishments for kick] --ban [punishments for ban]`"
        error = commands.BadArgument(f'this guild doesn\'t have any warn punishments! You can configure these by doing {signature}')
        try:
            punishments = data[str(ctx.guild.id)]['punishments']
        except KeyError:
            raise error
        else:
            if not punishments:
                raise error
        embed = discord.Embed(colour=self.bot.colour, description="Users will receive a...")
        for key, value in reversed(list(punishments.items())):
            embed.description += f"\n\n**{key}** at **{value}** warning(s)"
        embed.add_field(name="Info",
                        value=f"Configure these with {signature}\nView info on these with `{ctx.prefix}sgp info`")
        await ctx.send(embed=embed)

    @commands.command()
    @ct5k()
    async def apply(self, ctx, *, reason: str):
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.description = discord.utils.escape_markdown(reason)
        embed.title = "New mod application!"
        await self.bot.get_channel(753389607965556746).send(embed=embed)
        await ctx.message.add_reaction(ctx.tick())


def setup(bot):
    bot.add_cog(Moderation(bot))
