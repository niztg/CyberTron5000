import asyncio
from math import ceil

import discord
import humanize
from discord.ext import commands

from CyberTron5000.utils import paginator, lists
from CyberTron5000.utils.checks import check_mod_or_owner


# ≫


class Moderation(commands.Cog):
    """Commands for Moderation"""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":tickgreen:732660186560462958"
    
    def hierarchy(self, member):
        # check if I can action this user
        return member.guild.me.top_role > member.top_role and member != member.guild.owner
    
    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 5):
        """ Purges a given amount of messages with the default being 5 """
        await ctx.channel.purge(limit=(amount + 1))
        await ctx.send(f"{amount} messages have been cleared.", delete_after=3)
    
    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from a guild."""
        if not self.hierarchy(member):
            return await ctx.send('I cannot moderate that user')
        r = "No reason specified" if not reason else reason
        await member.send(
            f"Hello, you have been kicked from participating in {ctx.guild}. Please see your reason for removal: `{r}`")
        await member.kick(reason=r)
        await ctx.message.add_reaction(self.tick)
    
    @commands.command(help="Ban a member.")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from a guild."""
        if not self.hierarchy(member):
            return await ctx.send('I cannot moderate that user')
        r = "No reason specified" if not reason else reason
        await member.send(
            f"Hello, you have been kicked from participating in {ctx.guild}. Please see your reason for removal: `{r}`")
        await member.ban(reason=r)
        await ctx.message.add_reaction(self.tick)
    
    @commands.command(help="Unban a member.")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.message.add_reaction(emoji=":tickgreen:732660186560462958")
    
    @commands.group(help="Vote on something.", invoke_without_command=True)
    async def vote(self, ctx, *, message):
        valid_emojis = ['⬆️', '⬇️']
        author = ctx.message.author
        embed = discord.Embed(
            colour=self.client.colour, timestamp=ctx.message.created_at, title="Poll:", description=message
        )
        embed.set_footer(text=f"Started by {author}", icon_url=author.avatar_url)
        embed.add_field(name="Upvotes", value="1", inline=False)
        embed.add_field(name="Downvotes", value="1", inline=False)
        e = await ctx.send(embed=embed)
        for r in valid_emojis:
            await e.add_reaction(r)
        while True:
            names = ['Upvotes', 'Downvotes']
            done, pending = await asyncio.wait([
                self.client.wait_for("reaction_add"),
                self.client.wait_for("reaction_remove")
            ], return_when=asyncio.FIRST_COMPLETED)
            # m = await ctx.channel.fetch_message(e.id)
            res = done.pop().result()
            # print(res)
            if res[0].emoji in valid_emojis:
                index = valid_emojis.index(res[0].emoji)
                embed.set_field_at(index=index, name=names[index], value=f"{res[0].count}", inline=False)
                await e.edit(embed=embed)
    
    @vote.command(invoke_without_command=True)
    @commands.is_owner()
    async def ct5k(self, ctx, *, message):
        """Voting only in the CyberTron5000 help server (https://discord.gg/2fxKxJH)"""
        author = ctx.message.author
        embed = discord.Embed(
            colour=self.client.colour, timestamp=ctx.message.created_at, title="Poll:", description=message
        )
        embed.set_footer(text=f"Started by {author}", icon_url=author.avatar_url)
        await ctx.message.delete()
        string = str("<@&724429718882877531>")
        e = await ctx.send(string, embed=embed)
        for r in [':upvote:718895913342337036', ':downvote:718895842404335668']:
            await e.add_reaction(r)
    
    @commands.group(name='user-nick', help="Change a user's nickname.", aliases=['usernick', 'UnitedNations', 'un'],
                    invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def user_nick(self, ctx, member: discord.Member, *, name):
        if not self.hierarchy(member):
            return await ctx.send('I cannot moderate that user')
        await member.edit(nick=name)
        await ctx.message.add_reaction(emoji=":tickgreen:732660186560462958")
    
    @user_nick.command(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def default(self, ctx, member: discord.Member):
        """Change nickname back to default."""
        if not self.hierarchy(member):
            return await ctx.send('I cannot moderate that user')
        await member.edit(nick=member.name)
        await ctx.message.add_reaction(emoji=":tickgreen:732660186560462958")
    
    @commands.command()
    @check_mod_or_owner()
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
                actions.append(
                    f"{x.user.name} {lists.audit_actions[x.action]} {x.target} ({humanize.naturaltime(__import__('datetime').datetime.utcnow() - x.created_at)})")
            source = paginator.IndexedListSource(embed=discord.Embed(colour=self.client.colour).set_author(
                name=f"Last Audit Log Actions for {ctx.guild}",
                icon_url="https://cdn.discordapp.com/emojis/446847139977625620.png?v=1"), data=actions)
            menu = paginator.CatchAllMenu(source=source)
            await menu.start(ctx)
        except Exception as er:
            await ctx.send(f'{er.__class__.__name__}, {er}')
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, time: int = 10):
        min = time * 60
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
            await ctx.message.add_reaction(emoji=self.tick)
            await asyncio.sleep(min)
            if role not in member.roles:
                await ctx.send(f"{member.mention} unmuted automatically.")
                await member.remove_roles(role)
            else:
                pass
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, *, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="CyberMute")
        if not role:
            return await ctx.send("No one on this server was muted using me!")
        if role not in member.roles:
            return await ctx.send("This user is not muted!")
        await member.remove_roles(role)
        await ctx.message.add_reaction(emoji=self.tick)
        await ctx.send(f"{member.mention} has been unmuted.")
    
    @commands.group(invoke_without_command=True, aliases=['pre', 'prefix'], name='changeprefix')
    async def _prefix(self, ctx):
        """View the guild's current prefixes."""
        prefixes = self.client.prefixes.get(ctx.guild.id, ["c$"])
        embed = discord.Embed(color=self.client.colour)
        embed.set_author(name=f"Prefixes for {ctx.guild}", icon_url=ctx.guild.icon_url)
        embed.add_field(name="Prefixes",
                        value=f"{self.client.user.mention}, " + ", ".join([f"`{pre}`" for pre in prefixes]))
        embed.set_footer(
            text=f'Do "{ctx.prefix}prefix add" to add a new prefix, or "{ctx.prefix}prefix remove" to remove a prefix!')
        await ctx.send(embed=embed)
    
    @_prefix.command()
    @check_mod_or_owner()
    async def add(self, ctx, *, prefix):
        """Add a prefix for the guild."""
        prefixes = self.client.prefixes.get(ctx.guild.id, ["c$"])
        if prefix in prefixes:
            return await ctx.send(f"`{prefix}` is already a prefix for this guild!")
        if len(prefixes) > 15:
            return await ctx.send("This guild already has 15 prefixes! Please remove some before continuing.")
        await self.client.pg_con.execute("INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)", ctx.guild.id,
                                         prefix)
        try:
            self.client.prefixes[ctx.guild.id].append(prefix)
        except KeyError:
            self.client.prefixes[ctx.guild.id] = ["c$", prefix]
        await ctx.send(f'Success! `{prefix}` is now a prefix in {ctx.guild}!')
    
    @_prefix.command(aliases=['sp-add'])
    @check_mod_or_owner()
    async def spaceprefix_add(self, ctx, *, prefix):
        """Add a prefix for the guild that ends in a space."""
        prefixes = self.client.prefixes.get(ctx.guild.id, ["c$"])
        if prefix in prefixes:
            return await ctx.send(f"`{prefix}` is already a prefix for this guild!")
        if len(prefixes) > 15:
            return await ctx.send("This guild already has 15 prefixes! Please remove some before continuing.")
        await self.client.pg_con.execute("INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)", ctx.guild.id,
                                         f"{prefix} ")
        try:
            self.client.prefixes[ctx.guild.id].append(f"{prefix} ")
        except KeyError:
            self.client.prefixes[ctx.guild.id] = [f"{prefix} ", "c$"]
        await ctx.send(f'Success! `{prefix} ` is now a prefix in {ctx.guild}!')
    
    @_prefix.command(aliases=['rm'])
    @check_mod_or_owner()
    async def remove(self, ctx, *, prefix):
        """Remove a prefix for the guild."""
        prefixes = self.client.prefixes.get(ctx.guild.id)
        if prefix not in prefixes:
            return await ctx.send(f"`{prefix}` is not a prefix in {ctx.guild}!")
        await self.client.pg_con.execute("DELETE FROM prefixes WHERE prefix = $1 AND guild_id = $2", prefix,
                                         ctx.guild.id)
        try:
            self.client.prefixes[ctx.guild.id].remove(prefix)
        except KeyError:
            self.client.prefixes[ctx.guild.id] = []
        await ctx.send(f'`{prefix}` is no longer a prefix for {ctx.guild}')
    
    @_prefix.command(aliases=['sp-rm'])
    @check_mod_or_owner()
    async def spaceprefix_remove(self, ctx, *, prefix):
        """Remove a prefix for the guild."""
        prefixes = self.client.prefixes.get(ctx.guild.id)
        if f"{prefix} " not in prefixes:
            return await ctx.send(f"`{prefix} ` is not a prefix in {ctx.guild}!")
        await self.client.pg_con.execute("DELETE FROM prefixes WHERE prefix = $1 AND guild_id = $2", f"{prefix} ",
                                         ctx.guild.id)
        try:
            self.client.prefixes[ctx.guild.id].remove(f"{prefix} ")
        except KeyError:
            self.client.prefixes[ctx.guild.id] = []
        await ctx.send(f'`{prefix} ` is no longer a prefix for {ctx.guild}')
    
    @add.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"You need the **Kick Members** permission to run this command.")
    
    @remove.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"You need the **Kick Members** permission to run this command.")
            
    @commands.command(aliases=['elf'])
    async def emote_list_formatter(self, ctx, amount: int = 20):
        """Get a layout of emojis for your guild."""
        # we have to figure out how many messages to send
        # in this case we're gonna do one message for every 20 emojis in a guild
        messages = ['']
        messages *= ceil(len(ctx.guild.emojis)/amount) # now the list has all the messages we need to send, they're just empty.
        for i in range(len(messages)):
            start = i * amount
            end = amount * (i+1)
            # now we have the ranges for each message. we will edit each item in the list and then send them.
            for emoji in ctx.guild.emojis[start:end]:
                # formatting the items in the list
                messages[i] += f"{str(emoji)} • `<:{emoji.name}:{emoji.id}>`\n"
        if any([item for item in messages if len(item) > 1999]):
            return await ctx.send("The limit you chose was probably too long. Please try again with a smaller limit.")
        for message in messages:
            await ctx.send(message)


def setup(client):
    client.add_cog(Moderation(client))