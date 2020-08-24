from discord.ext import commands


class CyberContext(commands.Context):

    @staticmethod
    def tick(val: bool = True):
        return {
            True: "<:tickgreen:732660186560462958>",
            False: "<:redx:732660210132451369>"
        }.get(val)

