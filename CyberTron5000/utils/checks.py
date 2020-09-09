from discord.ext import commands

beta_squad = [569374429218603019, 670564722218762240]


def check_guild(guild):
    def predicate(ctx):
        return ctx.guild.id == guild

    return commands.check(predicate)


def check_mod_or_owner():
    def predicate(ctx):
        return ctx.author == ctx.bot.owner or ctx.author.permissions_in(ctx.channel).kick_members

    return commands.check(predicate)


def check_guild_and_admin(guild):
    def predicate(ctx):
        return ctx.guild.id == guild and ctx.message.author.permissions_in(channel=ctx.message.channel).administrator

    return commands.check(predicate)


def check_channel(channel):
    def predicate(ctx):
        return ctx.channel.id == channel

    return commands.check(predicate)


def betasquad():
    def predicate(ctx):
        return ctx.author == ctx.bot.owner or ctx.author.id in beta_squad

    return commands.check(predicate)


def bruh():
    def predicate(ctx):
        return ctx.guild.id != 653376332507643914

    return commands.check(predicate)


def mod():
    """Checks if they're a mod"""
    def predicate(ctx):
        return any(
            dict(ctx.channel.permissions_for(ctx.author)).get(perm) for perm in (
                'kick_members',
                'ban_members',
                'manage_messages',
                'manage_roles',
                'manage_channels'
            )
        )
    return commands.check(predicate)
