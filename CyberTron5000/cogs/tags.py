"""
Dedicated to thag
"""
from asyncio import TimeoutError

import discord
from discord.ext import commands

from CyberTron5000.utils.paginator import CatchAllMenu, IndexedListSource


class Tags(commands.Cog):
    """Tags are a way of storing data for later retrieval"""
    def __init__(self, bot):
        self.bot = bot
        self._tag_dict = bot._tag_dict

    @property
    def forbidden(self):
        ftags = list()
        for command in self.bot.get_command('tag').commands:
            ftags.append(command.name)
            if not (c := self.bot.get_command(f'{command}')):
                continue
            for alias in c.aliases:
                ftags.append(alias)
        return ftags

    def fetch_tag(self, ctx, tag):
        if not (guild_tags := self._tag_dict.get(ctx.guild.id)):
            raise ValueError(f'This guild does not have any tags!')
        try:
            return guild_tags[tag]['content']
        except KeyError:
            raise commands.BadArgument('This tag does not exist for this guild! (Note that tags are case-sensitive)')

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag=None):
        """Invokes a tag"""
        if not tag:
            return await ctx.send(f"do `{ctx.prefix}help tag` bruhv")
        try:
            to_send = self.fetch_tag(ctx, tag)
            await ctx.send(to_send)  # thag
        except ValueError as v:
            return await ctx.send(v)
        self._tag_dict[ctx.guild.id][tag]['uses'] += 1
        current_uses = await self.bot.pg_con.fetch("SELECT uses FROM tags WHERE name = $1 AND guild_id = $2", tag,
                                                   ctx.guild.id)
        uses = current_uses[0][0] or 0
        uses += 1
        await self.bot.pg_con.execute("UPDATE tags SET uses = $1 WHERE name = $2 AND guild_id = $3", uses, tag,
                                      ctx.guild.id)

    @tag.command(aliases=['create'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def add(self, ctx, tag, *, content):
        """Adds a tag"""
        if str(tag) in self.forbidden:
            return await ctx.send(
                "You have created a tag with a forbidden word! Forbidden words include: " + ", ".join(self.forbidden))
        if not self._tag_dict.get(ctx.guild.id):
            self._tag_dict[ctx.guild.id] = {}
        if self._tag_dict.get(ctx.guild.id).get(tag):
            return await ctx.send("This tag already exists for this guild!")
        self._tag_dict[ctx.guild.id][tag] = {'content': content, 'uses': 0, 'author': ctx.author.id}
        await self.bot.pg_con.execute(
            "INSERT INTO tags (user_id, guild_id, name, content, uses) VALUES ($1, $2, $3, $4, $5)", ctx.author.id,
            ctx.guild.id, tag, content, 0)
        await ctx.send(f"<:tickgreen:732660186560462958> Success! `{tag}` is now a tag in **{ctx.guild.name}**")

    @tag.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def edit(self, ctx, tag, *, new_content):
        """Edits a tag"""
        try:
            self.fetch_tag(ctx, tag)
        except Exception as error:
            return await ctx.send(error)
        if self._tag_dict[ctx.guild.id][tag]['author'] != ctx.author.id:
            raise commands.BadArgument('You do not own this tag!')
        self._tag_dict[ctx.guild.id][tag]['content'] = new_content
        await self.bot.pg_con.execute("UPDATE tags SET content = $1 WHERE name = $2 AND guild_id = $3", new_content,
                                      tag, ctx.guild.id)
        await ctx.send(f"<:tickgreen:732660186560462958> Success! Tag `{tag}` has been edited!")

    @commands.command(aliases=['all_tags', 'at'])
    async def guild_tags(self, ctx):
        """Shows you all the tags in the guild"""
        if not (guild_tags := self._tag_dict.get(ctx.guild.id)):
            return await ctx.send("This guild doesn't have any tags!")
        tags = sorted(guild_tags.items(), key=lambda x: x[1]['uses'], reverse=True)
        data = [f'{tag[0]} - {tag[1]["uses"]} uses' for tag in tags]
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name=f"All Tags in {ctx.guild}", icon_url=ctx.guild.icon_url)
        source = IndexedListSource(data=data, embed=embed, title="Tags")
        await CatchAllMenu(source=source).start(ctx)

    @tag.command()
    async def list(self, ctx, member: discord.Member = None):
        """Shows you all the tags of you or another member"""
        member = member or ctx.author
        if not (guild_tags := self._tag_dict.get(ctx.guild.id)):
            return await ctx.send("This guild doesn't have any tags!")
        tags = guild_tags.items()
        for tag in tags:
            if tag[1]['author'] != member.id:
                tags = tags.remove(tag)
        tags = sorted(tags, key=lambda x: x[1]['uses'], reverse=True)
        data = [f'{tag[0]} - {tag[1]["uses"]} uses' for tag in tags]
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name=f"All of {ctx.author}'s Tags in {ctx.guild}", icon_url=ctx.author.avatar_url)
        source = IndexedListSource(data=data, embed=embed, title="Tags")
        await CatchAllMenu(source=source).start(ctx)

    @commands.command()
    async def tags(self, ctx, member: discord.Member = None):
        """Shows you all the tags of you or another member"""
        member = member or ctx.author
        if not (guild_tags := self._tag_dict.get(ctx.guild.id)):
            return await ctx.send("This guild doesn't have any tags!")
        tags = guild_tags.items()
        for tag in tags:
            if tag[1]['author'] != member.id:
                tags = tags.remove(tag)
        tags = sorted(tags, key=lambda x: x[1]['uses'], reverse=True)
        data = [f'{tag[0]} - {tag[1]["uses"]} uses' for tag in tags]
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name=f"All of {ctx.author}'s Tags in {ctx.guild}", icon_url=ctx.author.avatar_url)
        source = IndexedListSource(data=data, embed=embed, title="Tags")
        await CatchAllMenu(source=source).start(ctx)

    @tag.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def make(self, ctx):
        """Makes a tag"""
        if not self._tag_dict.get(ctx.guild.id):
            self._tag_dict[ctx.guild.id] = {}
        await ctx.send(f"<a:loading:743537226503421973> Please enter a name for your tag...")
        try:
            message1 = await self.bot.wait_for('message', check=lambda x: x.author == ctx.author, timeout=30)
        except TimeoutError:
            return await ctx.send("<:redx:732660210132451369> Boo, you ran out of time!")
        if self._tag_dict.get(ctx.guild.id).get(message1.content):
            return await ctx.send("This tag already exists for this guild!")
        await ctx.send(
            f"<a:loading:743537226503421973> Your tag is called `{message1.content}`. Please enter the content of your tag...")
        try:
            message2 = await self.bot.wait_for('message', check=lambda x: x.author == ctx.author, timeout=30)
        except TimeoutError:
            return await ctx.send("<:redx:732660210132451369> Boo, you ran out of time!")
        self._tag_dict[ctx.guild.id][message1.content] = {'content': message2.content, 'uses': 0,
                                                          'author': ctx.author.id}
        await self.bot.pg_con.execute(
            "INSERT INTO tags (user_id, guild_id, name, content, uses) VALUES ($1, $2, $3, $4, $5)", ctx.author.id,
            ctx.guild.id, message1.content, message2.content, 0)
        await ctx.send(f"<:tickgreen:732660186560462958> Success! Tag `{message1.content}` created!")

    @tag.command(aliases=['rm', 'remove'])
    async def delete(self, ctx, *, tag):
        """Deletes a tag"""
        try:
            self.fetch_tag(ctx, tag)
        except Exception as error:
            return await ctx.send(error)
        if ctx.author.permissions_in(ctx.channel).kick_members or ctx.author.id == self._tag_dict[ctx.guild.id][tag]['author']:
            await self.bot.pg_con.execute("DELETE FROM tags WHERE name = $1 AND guild_id = $2", tag, ctx.guild.id)
            self._tag_dict[ctx.guild.id].pop(tag)
            await ctx.send(f"<:tickgreen:732660186560462958> Success! Tag `{tag}` deleted!")
        else:
            await ctx.send("You cant delete that tag!")

    @tag.command()
    async def info(self, ctx, *, tag):
        """Shows info on a tag"""
        try:
            self.fetch_tag(ctx, tag)
        except Exception as error:
            return await ctx.send(error)
        data = self._tag_dict[ctx.guild.id][tag]
        author = self.bot.get_user(data['author']) or await self.bot.fetch_user(data['author'])
        embed = discord.Embed(colour=self.bot.colour)
        embed.title = tag
        embed.description = f"<:author:734991429843157042> **{author}**\n"
        embed.description += f"Uses: **{data['uses']}**"
        embed.set_author(name=str(author), icon_url=author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Tags(bot))
