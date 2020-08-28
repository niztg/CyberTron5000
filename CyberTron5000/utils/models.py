import json
from datetime import datetime as dt


class InfractionUser:
    """A template for a warning user"""

    def __init__(self, guild_id, user_id):
        self._guild = guild_id
        self._user = user_id
        self._data = self.collect_data()

    def collect_data(self):
        """The base data for this user"""
        with open('json_files/infractions.json') as f:
            data = json.load(f)
        if not (resp := data.get(str(self._guild))):
            data[str(self._guild)] = {str(self._user): []}
            with open('json_files/infractions.json', 'w') as f:
                json.dump(data, f, indent=4)
            return []
        try:
            return resp[str(self._user)]
        except KeyError:
            resp[str(self._user)] = []
            with open('json_files/infractions.json', 'w') as f:
                json.dump(resp, f, indent=4)
            return []

    def all_infractions(self):
        """Returns a list of all of their infractions in the Infraction object referenced below"""
        infractions = []
        for infrac in self._data:
            infractions.append(Infraction(infrac))
        return infractions

    def add_infraction(self, reason="No reason provided."):
        """Adds an infraction to them"""
        self._data.append({"reason": reason, "infraction_number": len(self._data) + 1, "is_null": False, "created": str(dt.utcnow())})

    def finalize(self):
        """Finalizes any changes made to their profile."""
        with open('json_files/infractions.json') as f:
            data = json.load(f)
        data[str(self._guild)] = {str(self._user): self._data}
        with open('json_files/infractions.json', 'w') as f:
            json.dump(data, f, indent=4)

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
        self.infraction_number = data.get('infraction_number')
        self.is_null = data.get('is_null')

    def __int__(self):
        return self.infraction_number

    def __bool__(self):
        return self.is_null

    def __repr__(self):
        return f"<Infraction={self.infraction_number} reason={self.reason} null={self.is_null} created={self.created}>"

    def edit_infraction(self, reason):
        self._data['reason'] = reason
        with open('json_files/infractions.json', 'w') as f:
            json.dump(self._data, f, indent=4)

    def nullify(self):
        self._data['is_null'] = True
        with open('json_files/infractions.json', 'w') as f:
            json.dump(self._data, f, indent=4)

    @classmethod
    def by_infraction_no(cls, guild_id, user_id, infraction_number):
        with open('json_files/infractions.json') as f:
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
    punishments_dict = {}
    for key, value in options.items():
        if not isinstance(value, int):
            raise AttributeError("All of your values must be integers!")
        punishments_dict['key'] = value
    with open('json_files/infractions.json', 'r') as f:
        data = json.load(f)
    try:
        data[str(guild_id)]['punishments'] = punishments_dict
    except KeyError:
        data[str(guild_id)] = {"punishments": punishments_dict}
    with open('json_files/infractions.json', 'w') as f:
        json.dump(data, f, indent=4)