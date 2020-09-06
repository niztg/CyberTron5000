import json
from datetime import datetime as dt
from discord import Embed, Colour


class InfractionUser:
    """A template for a warning user"""

    def __init__(self, guild_id, user_id):
        self._guild = guild_id
        self._user = user_id
        self._data = self.collect_data()

    def collect_data(self):
        """The base data for this user"""
        with open('./json_files/infractions.json') as f:
            data = json.load(f)
        resp = data.get(str(self._guild))
        if not resp:
            return []
        try:
            return resp[str(self._user)]
        except KeyError:
            return []

    def all_infractions(self):
        """Returns a list of all of their infractions in the Infraction object referenced below"""
        infractions = []
        for infrac in self._data:
            infractions.append(Infraction(infrac))
        return infractions

    def add_infraction(self, reason="No reason provided."):
        """Adds an infraction to them"""
        infraction = {"reason": reason, "infraction_number": len(self._data) + 1, "is_null": False,
                      "created": str(dt.utcnow())}
        self._data.append(infraction)
        with open('./json_files/infractions.json') as f:
            data = json.load(f)
        if not data.get(str(self._guild)):
            data[str(self._guild)] = {}
        try:
            data[str(self._guild)][str(self._user)].append(infraction)
        except KeyError:
            data[str(self._guild)][str(self._user)] = [infraction]

        with open('./json_files/infractions.json', 'w') as fp:
            json.dump(data, fp, indent=4)
        return Infraction(infraction)

    @property
    def valid_infractions(self):
        """Shows a list of infractions that are valid, i.e. not null."""
        return [i for i in self.all_infractions() if not bool(i)]

    @property
    def num_infractions(self):
        return len(self.all_infractions())

    @property
    def num_valid_infractions(self):
        """The number of valid infractions they have."""
        return len(self.valid_infractions)

    # TODO: determine how to add a punishment with this.


class Infraction:
    def __init__(self, data):
        self._data = data
        self.reason = data.get('reason')
        self.infraction_number = data.get('infraction_number')  # idk why
        self.is_null = data.get('is_null')

    def __int__(self):
        return self.infraction_number

    def __bool__(self):
        return self.is_null

    def __repr__(self):
        return f"<Infraction={self.infraction_number} reason={self.reason} null={self.is_null} created={self.created}>"

    def edit(self, reason):
        try:
            with open('./json_files/infractions.json') as f:
                data = json.load(f)
            index = data[str(self._guild)][str(self._user)].index(self._data)
            self._data['reason'] = reason
            data[str(self._guild)][str(self._user)][index] = self._data
            with open('./json_files/infractions.json', 'w') as f:
                json.dump(data, f, indent=4)
            self.reason = reason
        except:
            raise AttributeError()

    def nullify(self):
        try:
            with open('./json_files/infractions.json') as f:
                data = json.load(f)
            index = data[str(self._guild)][str(self._user)].index(self._data)
            self._data['is_null'] = not self.is_null
            data[str(self._guild)][str(self._user)][index] = self._data
            with open('./json_files/infractions.json', 'w') as f:
                json.dump(data, f, indent=4)
            self.is_null = not self.is_null
        except:
            raise AttributeError('This error doesn\'t exist!')

    @classmethod
    def by_infraction_no(cls, guild_id, user_id, infraction_number):
        cls._guild = guild_id
        cls._user = user_id
        with open('./json_files/infractions.json') as f:
            data = json.load(f)
        try:
            data = data[str(guild_id)][str(user_id)]
        except KeyError:
            raise AttributeError("This guild and/or member has no infractions!")
        try:
            index = [item['infraction_number'] for item in data].index(infraction_number)
        except:
            raise AttributeError("This infraction number doesn't exist for this user!")
        return cls(data[index])

    @property
    def created(self):
        return dt.strptime(self._data.get('created'), '%Y-%m-%d %H:%M:%S.%f')


def set_infraction_punishments(guild_id, **options):
    if any(item not in ['mute', 'kick', 'ban'] for item in options.keys()):
        raise AttributeError('You have passed in invalid punishments! Valid punishments include mute, kick, ban.')
    for key, value in options.items():
        if not isinstance(value, int):
            raise ValueError("All of your values must be integers!")
    with open('./json_files/infractions.json', 'r') as f:
        data = json.load(f)
    if not data.get(str(guild_id)):
        data[str(guild_id)] = {}
    data[str(guild_id)]['punishments'] = dict(options)
    with open('./json_files/infractions.json', 'w') as f:
        json.dump(data, f, indent=4)


class CyberColours(Colour):
    @classmethod
    def main(cls):
        return cls(0x00dcff)


class CyberEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colour = kwargs.get('colour') or kwargs.get('color') or CyberColours.main()
