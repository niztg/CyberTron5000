import discord

class Fighter:
    def __init__(self, member: discord.Member):
        self.name = member.display_name
        self.health = 100
        self.self = member

    def update_heath(self, amt: int):
        self.health += amt
        return amt

    @property
    def dead(self):
        return self.health <= 0

    def heal(self):
        if self.health == 100:
            raise ValueError("You are already at max health, you can't heal now.")
        else:
            amt = 100 - self.health
            heal = random.randint(1, amt)
            self.update_heath(heal)
            return heal

    def __repr__(self):
        return "{0.name} ♥️ **{0.health}**".format(self)