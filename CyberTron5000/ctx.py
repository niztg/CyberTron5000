from discord.ext import commands


class CyberContext(commands.Context):

    def tick(self, val: bool = True):
        # inspired by Rapptz' RoboDanny
        # (no code was used)
        return {
            True: self.bot.get_emoji(732660186560462958),
            False: self.bot.get_emoji(732660210132451369)
        }.get(val)

