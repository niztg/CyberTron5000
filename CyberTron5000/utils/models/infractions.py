import json
from datetime import datetime as dt

__all__ = (
    'FILENAME',
    'InfractionUser',
    'Infraction',
    'set_infraction_punishments'
)

FILENAME = './json_files/infractions.json'


class InfractionUser:
    """A template for a warning user"""
    __slots__ = (
        '_guild',
        '_user',
        '_data'
    )

    def __init__(self, guild_id, user_id):
        self._guild = guild_id
        self._user = user_id
        self._data = self.collect_data()

    def collect_data(self):
        """The base data for this user"""
        with open(FILENAME) as f:
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

    def __iter__(self):
        return iter(list(self.all_infractions()))

    def add_infraction(self, reason="No reason provided."):
        """Adds an infraction to them"""
        infraction = {"reason": reason, "infraction_number": len(self._data) + 1, "is_null": False,
                      "created": str(dt.utcnow())}
        self._data.append(infraction)
        with open(FILENAME) as f:
            data = json.load(f)
        if not data.get(str(self._guild)):
            data[str(self._guild)] = {}
        try:
            data[str(self._guild)][str(self._user)].append(infraction)
        except KeyError:
            data[str(self._guild)][str(self._user)] = [infraction]

        with open(FILENAME, 'w') as fp:
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

    def determine_punishment(self):
        with open(FILENAME) as f:
            data = json.load(f)
        try:
            punishments = data[str(self._guild)]['punishments']
        except KeyError:
            return None
        punishments = punishments.items()
        try:
            index = [p[1] for p in punishments].index(self.num_valid_infractions)
        except:
            return None
        return list(punishments)[index][0]

    def clear_punishments(self):
        with open(FILENAME) as f:
            data = json.load(f)
        try:
            data[str(self._guild)][str(self._user)] = []
        except:
            pass
        with open(FILENAME, 'w') as f:
            json.dump(data, f, indent=4)


class Infraction:
    """The model for an infraction"""
    __slots__ = (
        '_data',
        'reason',
        'infraction_number',
        'is_null'
    )

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
            with open(FILENAME) as f:
                data = json.load(f)
            index = data[str(self._guild)][str(self._user)].index(self._data)
            self._data['reason'] = reason
            data[str(self._guild)][str(self._user)][index] = self._data
            with open(FILENAME, 'w') as f:
                json.dump(data, f, indent=4)
            self.reason = reason
        except:
            raise AttributeError()

    def nullify(self):
        try:
            with open(FILENAME) as f:
                data = json.load(f)
            index = data[str(self._guild)][str(self._user)].index(self._data)
            self._data['is_null'] = not self.is_null
            data[str(self._guild)][str(self._user)][index] = self._data
            with open(FILENAME, 'w') as f:
                json.dump(data, f, indent=4)
            self.is_null = not self.is_null
        except:
            raise AttributeError('This error doesn\'t exist!')

    @classmethod
    def by_infraction_no(cls, guild_id, user_id, infraction_number):
        cls._guild = guild_id
        cls._user = user_id
        with open(FILENAME) as f:
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
    with open(FILENAME, 'r') as f:
        data = json.load(f)
    if not data.get(str(guild_id)):
        data[str(guild_id)] = {}
    data[str(guild_id)]['punishments'] = dict(options)
    with open(FILENAME, 'w') as f:
        json.dump(data, f, indent=4)
