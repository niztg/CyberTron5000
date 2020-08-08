import ast

from discord.ext import commands

beta_squad = [569374429218603019, 670564722218762240]


def check_guild(guild):
    def predicate(ctx):
        if ctx.guild.id == guild:
            return True
        else:
            return False
    
    return commands.check(predicate)


def check_admin_or_owner():
    def predicate(ctx):
        if ctx.message.author.id == 350349365937700864:
            return True
        elif ctx.message.author.permissions_in(channel=ctx.message.channel).kick_members:
            return True
        else:
            return False
    
    return commands.check(predicate)


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


def check_guild_and_admin(guild):
    def predicate(ctx):
        if ctx.guild.id == guild and ctx.message.author.permissions_in(channel=ctx.message.channel).administrator:
            return True
        else:
            return False
    
    return commands.check(predicate)


def check_guild_and_channel(channel):
    def predicate(ctx):
        if ctx.channel.id == channel:
            return True
        else:
            return False
    
    return commands.check(predicate)


def betasquad():
    def predicate(ctx):
        if ctx.author.id == 350349365937700864:
            return True
        elif ctx.author.id in beta_squad:
            return True
        return False
    
    return commands.check(predicate)
