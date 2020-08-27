import json


class InfractionUser:
    """A template for a warning user"""

    def __init__(self, guild_id, user_id):
        self._guild = guild_id
        self._user = user_id
        self._data = self.collect_data()

    def collect_data(self):
        with open('json_files/infractions.json') as f:
            data = json.load(f)
        return data[str(self._guild)][str(self._user)]

    def all_infractions(self):
        infractions = []
        for infrac in self._data:
            infractions.append(Infraction(infrac))
        return infractions

    def add_infraction(self, reason="No reason provided."):
        self._data.append({"reason": reason, "infraction_number": len(self._data)+1})
        with open('json_files/infractions.json', 'w') as f:
            json.dump(self._data, f, indent=4)


class Infraction:
    def __init__(self, data):
        self._data = data
        self.reason = data.get('reason')
        self.infraction_number = data.get('infraction_number')

    def edit_infraction(self, reason):
        self._data['reason'] = reason
        with open('json_files/infractions.json', 'w') as f:
            json.dump(self._data, f, indent=4)

    @classmethod
    def by_infraction_no(cls, guild_id, user_id, infraction_number):
        with open('json_files/infractions.json') as f:
            data = json.load(f)
        data = data[str(guild_id)][str(user_id)]
        index = [item['infraction_number'] for item in data].index(infraction_number)
        return cls(data[index])