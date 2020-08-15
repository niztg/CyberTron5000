import asyncio
import itertools
from contextlib import suppress

import discord
from discord.ext import commands

from CyberTron5000.utils import paginator


class CyberTronHelpCommand(commands.HelpCommand):
    """
    Subclassed help FTW!
    """

    def __init__(self):
        """
        Sets some attributes.
        """
        super().__init__(
            command_attrs={
                'help': 'Shows info about the bot, a command, or a category',
                'aliases': ['?']
            }
        )
        self._help_dict = {"<argument>": "This means the argument is **required**",
                           "[argument]": "This means the argument is **optional**",
                           "[A|B]": "This means it could be either **A or B**",
                           "[argument...]": "This means you can have **multiple arguments**"}

    def get_command_signature(self, command):
        """
        Lines 35-45 used from Rapptz' R.Danny repository provided by the MIT License
        https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L125-L135
        Copyright (c) 2015 Rapptz
        """
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '•'.join(command.aliases)
            fmt = f'{command.name}•{aliases}'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{self.clean_prefix}{alias} {command.signature}'

    def command_not_found(self, string):
        """
        Just makes a custom error when command is not found.
        :param string:
        :return:
        """
        return f"Command/category `{string}` not found!"

    async def send_bot_help(self, mapping):
        """
        Sends the actual help message
        :param mapping:
        :return:
        """

        def key(c):
            return c.cog_name or '\u200bUncategorized Commands'

        total = 0
        embed = discord.Embed(colour=self.context.bot.colour,
                              description=f'You can do `{self.clean_prefix}help [command/category]` for more info.\n\n')
        entries = await self.filter_commands(self.context.bot.commands, sort=True, key=key)
        for cg, cm in itertools.groupby(entries, key=key):
            cats = []
            cm = sorted(cm, key=lambda c: c.name)
            cats.append(f'**{cg}**\n{" • ".join([f"{c.name}" for c in cm])}\n')
            embed.description += "\n".join(cats)
            total += len([c for c in cm])
        embed.set_author(name=f"CyberTron5000 Commands (Total {total})")
        msg = await self.context.send(embed=embed)
        embed_dict = {
            ":info:731324830724390974": discord.Embed(colour=self.context.bot.colour,
                                                      description="<argument> - This means the argument is **required.**\n[argument] - This means the argument is **optional.**\n[A|B] - This means that it can be either **A or B.**\n[argument...] - This means you can have **multiple arguments.**\nNow that you know the basics, it should be noted that...\n**You do not type in the brackets!**"),
            ":redo:741793178704937000": embed
        }
        valid_reactions = [*embed_dict.keys()] + [':stop_button:731316755485425744']

        def check(reaction, user):
            str_reaction = ''
            for x in str(reaction):
                if x in ('<', '>'):
                    continue
                else:
                    str_reaction += x
            return str_reaction in valid_reactions and user == self.context.author and user.bot is False and reaction.message.id == msg.id

        for i in valid_reactions:
            await msg.add_reaction(i)
        with suppress(Exception):
            while True:
                done, pending = await asyncio.wait(
                    [self.context.bot.wait_for('reaction_add', timeout=300, check=check),
                     self.context.bot.wait_for('reaction_remove', timeout=300, check=check)],
                    return_when=asyncio.FIRST_COMPLETED)
                data = done.pop().result()
                if str(data[0]) == '<:stop_button:731316755485425744>':
                    await msg.delete()
                    await self.context.message.add_reaction(emoji=":tickgreen:732660186560462958")
                    break
                else:
                    str_reaction = ''
                    for x in str(data[0]):
                        if x in ('<', '>'):
                            continue
                        else:
                            str_reaction += x
                    e = embed_dict.get(str_reaction)
                    await msg.edit(embed=e)

    async def send_cog_help(self, cog):
        """
        Help for a cog.
        :param cog:
        :return:
        """
        cog_doc = cog.__doc__ or " "
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        foo = [f"→ `{self.get_command_signature(c)}` {c.help or 'No help provided for this command'}" for c in entries]
        embed = discord.Embed(description=f"{cog_doc}", colour=self.context.bot.colour).set_author(
            name=f"{cog.qualified_name} Commands (Total {len(entries)})")
        if entries and len(entries) > 6:
            source = paginator.IndexedListSource(show_index=False, embed=embed, data=foo, per_page=6, title='Commands')
            menu = paginator.CatchAllMenu(source=source)
            menu.add_info_fields(self._help_dict)
            await menu.start(self.context)
        else:
            if foo:
                embed.add_field(name="Commands", value="\n".join(foo))
            await self.context.send(embed=embed)

    async def send_command_help(self, command):
        """
        Help for a command.
        :param command:
        :return:
        """
        embed = discord.Embed(title=self.get_command_signature(command), colour=self.context.bot.colour,
                              description=command.help or "No help provided for this command.")
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        """
        Help for a subcommand group.
        :param group:
        :return:
        """
        sc = []
        entries = await self.filter_commands(group.commands)
        embed = discord.Embed(title=self.get_command_signature(group), colour=self.context.bot.colour)
        for c in entries:
            sc.append(f"→ `{self.get_command_signature(c)}` {c.help or 'No help provided.'}")
        embed.description = f"{group.help}"
        if entries and len(entries) > 6:
            source = paginator.IndexedListSource(show_index=False, data=sc, embed=embed, per_page=6,
                                                 title='Subcommands')
            menu = paginator.CatchAllMenu(source=source)
            menu.add_info_fields(self._help_dict)
            await menu.start(self.context)
        else:
            if sc:
                embed.add_field(name="Subcommands", value="\n".join(sc))
            await self.context.send(embed=embed)


class Help(commands.Cog):
    """Help Commands"""

    def __init__(self, bot):
        """
        Sets up the whole help command thing
        :param bot:
        """
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = CyberTronHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        """
        ah yes, this.
        :return:
        """
        self.bot.help_command = self._original_help_command

    @commands.group(invoke_without_command=True)
    async def cogs(self, ctx):
        """Shows you every cog"""
        embed = discord.Embed(colour=self.bot.colour)
        embed.title = "All Cogs"
        embed.description = " "
        for x, y in self.bot.cogs.items():
            embed.description += f"`{x}` - {y.description} (**{len(y.get_commands())}** commands)\n"
        await ctx.send(embed=embed)

    @commands.command(name='paginated_help', aliases=['phelp'])
    async def phelp(self, ctx, *, command=None):
        """
        If you don't like the regular help command

        """
        embeds = []
        use = self.bot.get_command(command) if command else None
        lcogs = [str(cog) for cog in self.bot.cogs]
        if not command:
            for name, obj in self.bot.cogs.items():
                embed = discord.Embed(title=f"{name} Commands", colour=self.bot.colour)
                cmds = []
                for cmd in obj.get_commands():
                    cmds.append(f"→ `{cmd.name} {cmd.signature}` | {cmd.help}")
                embed.description = '\n'.join(cmds)
                if cmds:
                    embeds.append(embed)
                else:
                    continue
            pages = paginator.CatchAllMenu(paginator.EmbedSource([discord.Embed(colour=self.bot.colour,
                                                                                title=f'{self.bot.user.name} Help',
                                                                                description=f'Do `{ctx.prefix}help command/cog` for more info').set_image(
                url=self.bot.user.avatar_url)] + embeds))
            await pages.start(ctx)
        elif command in lcogs:
            embed = discord.Embed(colour=self.bot.colour, title=f'{command.capitalize()} Help')
            embed.description = '\n'.join(
                [f"→ `{cmd.name} {cmd.signature}` | {cmd.help}" for cmd in self.bot.cogs[command].get_commands()])
            await ctx.send(embed=embed)
        elif command and use:
            help_msg = use.help or "No help provided for this command"
            parent = use.full_parent_name
            if len(use.aliases) > 0:
                aliases = '|'.join(use.aliases)
                cmd_alias_format = f'{use.name}|{aliases}'
                if parent:
                    cmd_alias_format = f'{parent} {cmd_alias_format}'
                alias = cmd_alias_format
            else:
                alias = use.name if not parent else f'{parent} {use.name}'
            embed = discord.Embed(title=f"{alias} {use.signature}", description=help_msg, colour=self.bot.colour)
            if isinstance(use, commands.Group):
                embed = discord.Embed(title=f"{alias} {use.signature}", description=help_msg,
                                      colour=self.bot.colour)
                for sub_cmd in use.commands:
                    u = '\u200b'
                    embed.add_field(
                        name=f"{use.name} {sub_cmd.name}{'|' if sub_cmd.aliases else u}{'| '.join(sub_cmd.aliases)} {sub_cmd.signature}",
                        value=f"{sub_cmd.help}", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=embed)
        elif command not in lcogs or command and not use:
            await ctx.send("not found")


def setup(bot):
    bot.add_cog(Help(bot))
