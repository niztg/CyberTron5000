import ast
import asyncio
from datetime import datetime as dt
import json
import random
import subprocess
import sys

import humanize
import discord
from discord.ext import commands, flags

from CyberTron5000.utils import cyberformat, lists
from CyberTron5000.utils.models import Infraction, InfractionUser, set_infraction_punishments

null = '<:ticknull:732660186057015317>'
reload = '<:reload:732674920873459712>'


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._ = None
        
    async def cog_check(self, ctx):
        return ctx.author == ctx.bot.owner
    
    @commands.group(invoke_without_command=True, aliases=['developer', 'd'], help="Developer commands")
    async def dev(self, ctx):
        pass
    
    @dev.command(aliases=["e", "evaluate"], name='eval', help="Evaluates a function.")
    async def eval_fn(self, ctx, *, cmd):
        global result
        try:
            fn_name = "_eval_expr"
            cmd = cyberformat.codeblock(cmd)
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'me': ctx.guild.me,
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'get': discord.utils.get,
                'ctx': ctx,
                'asyncio': asyncio,
                '__import__': __import__,
                'author': ctx.author,
                'guild': ctx.guild,
                'channel': ctx.channel,
                'send': ctx.send,
                '_': self._,
            }
            try:
                exec(compile(parsed, filename="<eval>", mode="exec"), env)
                result = (await eval(f"{fn_name}()", env))
            except Exception as error:
                return await ctx.send(embed=discord.Embed(color=self.bot.colour,
                                                          description=f"{error.__class__.__name__}```py\n{error}\n```"))
        except Exception as error:
            return await ctx.send(embed=discord.Embed(color=self.bot.colour,
                                                      description=f"{error.__class__.__name__}```py\n{error}\n```"))
        
        embed = discord.Embed(color=self.bot.colour)
        embed.description = f"```py\n{result}\n```"
        await ctx.message.add_reaction(emoji=ctx.tick())
        await ctx.send(embed=embed)
        self._ = result
        
    @dev.command()
    async def repl(self, ctx):
        """Starts a REPL session"""
        global result
        await ctx.send(embed=discord.Embed(description="```Starting REPL Session```", colour=self.bot.colour))
        while True:
            ms = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            if ms.content.lower().startswith(f"{ctx.prefix}exit"):
                return await ctx.send(
                    embed=discord.Embed(description="```Exiting REPL Session```", color=self.bot.colour))
            try:
                fn_name = "_eval_expr"
                cmd = cyberformat.codeblock(ms.content)
                cmd = cmd.strip("` ")
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
                body = f"async def {fn_name}():\n{cmd}"
                parsed = ast.parse(body)
                body = parsed.body[0].body
                insert_returns(body)
                env = {
                    'me': ctx.guild.me,
                    'bot': ctx.bot,
                    'discord': discord,
                    'commands': commands,
                    'get': discord.utils.get,
                    'ctx': ctx,
                    'asyncio': asyncio,
                    '__import__': __import__,
                    'author': ctx.author,
                    'guild': ctx.guild,
                    'channel': ctx.channel,
                    '_': self._,
                }
                try:
                    exec(compile(parsed, filename="<ast>", mode="exec"), env)
                    result = (await eval(f"{fn_name}()", env))
                except Exception as error:
                    await ctx.send(embed=discord.Embed(color=self.bot.colour,
                                                       description=f"{error.__class__.__name__}```py\n{error}\n```"))
                    continue
            except Exception as error:
                await ctx.send(embed=discord.Embed(color=self.bot.colour,
                                                   description=f"{error.__class__.__name__}```py\n{error}\n```"))
                continue
            await ctx.send(f'{result}')
            self._ = result

    @dev.command(help="Loads Cogs", aliases=['l'])
    async def load(self, ctx, *extension):
        if not extension:
            for file in self.bot.ext:
                try:
                    self.bot.load_extension(file)
                except:
                    continue
            embed = discord.Embed(
                description="\n".join([f"{ctx.tick()} `cogs.{f[19:]}`" for f in self.bot.ext]),
                colour=self.bot.colour)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji=ctx.tick())

        else:
            cogs = [c[19:] for c in self.bot.ext]
            for i in extension:
                if i not in cogs:
                    return await ctx.send(f"**{i}** is not a valid cog!")

            for f in extension:
                self.bot.load_extension(f'CyberTron5000.cogs.{f}')
            a = []
            for x in cogs:
                if x in extension:
                    a.append(f"{ctx.tick()} `cogs.{x}`")
                else:
                    a.append(f"{null} `cogs.{x}`")

            await ctx.message.add_reaction(emoji=ctx.tick())
            await ctx.send(embed=discord.Embed(description="\n".join(a), colour=self.bot.colour))
    
    @dev.command(help="Unloads Cogs", aliases=['ul'])
    async def unload(self, ctx, *extension):
        if not extension:
            for file in self.bot.ext:
                try:
                    self.bot.unload_extension(file)
                except:
                    continue
            embed = discord.Embed(
                description="\n".join([f"{ctx.tick(False)} `cogs.{f[19:]}`" for f in self.bot.ext]),
                colour=self.bot.colour)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji=ctx.tick())
        
        else:
            cogs = [c[19:] for c in self.bot.ext]
            for i in extension:
                if i not in cogs:
                    return await ctx.send(f"**{i}** is not a valid cog!")
            
            for f in extension:
                self.bot.unload_extension(f'CyberTron5000.cogs.{f}')
            a = []
            for x in cogs:
                if x in extension:
                    a.append(f"{ctx.tick(False)} `cogs.{x}`")
                else:
                    a.append(f"{null} `cogs.{x}`")
            
            await ctx.message.add_reaction(emoji=ctx.tick())
            await ctx.send(embed=discord.Embed(description="\n".join(a), colour=self.bot.colour))
    
    @dev.command(help="Reloads Cogs", aliases=['rl'])
    async def reload(self, ctx, *extension):
        if not extension:
            for file in self.bot.ext:
                try:
                    self.bot.reload_extension(file)
                except:
                    continue
            embed = discord.Embed(
                description="\n".join([f"{reload} `cogs.{f[19:]}`" for f in self.bot.ext]),
                colour=self.bot.colour)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji=ctx.tick())

        else:
            cogs = [c[19:] for c in self.bot.ext]
            for i in extension:
                if i not in cogs:
                    return await ctx.send(f"**{i}** is not a valid cog!")

            for f in extension:
                self.bot.reload_extension(f'CyberTron5000.cogs.{f}')
            a = []
            for x in cogs:
                if x in extension:
                    a.append(f"{reload} `cogs.{x}`")
                else:
                    a.append(f"{null} `cogs.{x}`")

            await ctx.message.add_reaction(emoji=ctx.tick())
            await ctx.send(embed=discord.Embed(description="\n".join(a), colour=self.bot.colour))
    
    @dev.command(help="Logs CyberTron5000 out.")
    async def logout(self, ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{self.bot.user.name} logging out. Goodbye World! 🌍",
                                color=self.bot.colour))
        await self.bot.logout()
    
    @dev.command()
    async def restart(self, ctx):
        await ctx.message.add_reaction(emoji=ctx.tick())
        await self.bot.logout()
        subprocess.call([sys.executable, "ct5k.py"])
    
    @dev.command(aliases=['nu', 'update'])
    async def news_update(self, ctx, *, message):
        """Update the current news."""
        number = await self.bot.db.fetch("SELECT number FROM news")
        number = number[0][0] or 0
        number += 1
        await self.bot.db.execute("UPDATE news SET message = $1, number = $2", message, number)
        await ctx.send(embed=discord.Embed(colour=self.bot.colour, description=f"**News Updated To:**\n{message}"))

    @dev.command()
    async def sql(self, ctx, *, statement):
        statement = cyberformat.codeblock(statement, lang='sql')
        res = await self.bot.db.fetch(statement)
        await ctx.send(res)

    @dev.command()
    @commands.cooldown(1, 45, commands.BucketType.channel)
    async def timer(self, ctx, seconds: int = 60):
        le_seconds = list(range(seconds))
        embed = discord.Embed(colour=0x5643fd, title="Ur Mom", description=f'{seconds}')
        msg = await ctx.send(embed=embed)
        for num in le_seconds[::-1]:
            embed.description = f'{num}'
            await msg.edit(embed=embed)
            if num == 1:
                break
            await asyncio.sleep(1)
            continue
        embed.description = f"Done!\nCounted from **{seconds}** successfully"
        await msg.edit(embed=embed)

    @dev.command()
    async def rng(self, ctx, no: int, no2: int):
        await ctx.send(random.randint(no, no2))

    @dev.command()
    async def snipe_cache(self, ctx, channel: discord.TextChannel = None):
        l = list()
        with open('./json_files/snipes.json') as f:
            data = json.load(f)
        if not channel:
            for x in data.values():
                l += x
            await ctx.send(f"I have cached **{len(l)}** deleted message(s) across **{len(data.keys())}** channels!")
        else:
            try:
                await ctx.send(f"I have cached **{len(data[str(channel.id)])}** deleted message(s) in {channel}")
            except KeyError:
                await ctx.send(f"I have cached **0** deleted message(s) in {channel}")

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided."):
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

    @warn.command()
    async def list(self, ctx, member: discord.Member = None):
        command = self.bot.get_command('infractions')
        await ctx.invoke(command, member)

    @commands.command()
    async def infractions(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user = InfractionUser(ctx.guild.id, member.id)
        embed = discord.Embed(
            colour=self.bot.colour
        )
        for infraction in user.all_infractions():
            embed.add_field(name=f"**Infraction #{infraction.infraction_number}:**",
                            value=f"> {infraction.reason}\nIssued **{humanize.naturaltime(dt.utcnow() - infraction.created)}**\n{ctx.tick(infraction.is_null)} **Is Null?**")
        embed.set_author(name=f"All of {member.display_name}'s warnings", icon_url=member.avatar_url)
        embed.description = f"All Infractions: `{user.num_infractions}`\nValid Infractions: `{user.num_valid_infractions}`\n\n"
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            embed.remove_field(len(embed.fields) - 1)

    @warn.command()
    async def nullify(self, ctx, member: discord.Member, infraction_no: int):
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
    async def edit(self, ctx, member: discord.Member, number: int, *, reason):
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
    @commands.is_owner()
    async def set_guild_punishments(self, ctx, **flags):
        new_dict = {key: value for key, value in flags.items() if value}
        set_infraction_punishments(ctx.guild.id, **new_dict)
        single, double = "'", '"'
        await ctx.send(
            "Infraction Punishments edited to:\n" + f"```json\n{str(new_dict).replace(single, double)}\n```")

    @set_guild_punishments.command()
    async def info(self, ctx):
        embed = discord.Embed(
            colour=self.bot.colour,
            title=f"Infraction Punishment Info",
            description="\n\n".join(
                [f"**{key}**:\n{value.format(ctx.prefix)}" for key, value in lists.INFRACTION_DESCRIPTIONS.items()])
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Developer(bot))
