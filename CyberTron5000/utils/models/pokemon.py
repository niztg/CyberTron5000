import asyncio

import aiohttp

from CyberTron5000.utils.lists import TYPES, STAT_NAMES

__all__ = (
    'Pokemon'
)


class Pokemon:
    __slots__ = (
        'pokemon',
        'session',
        'name',
        'id',
        'types',
        'species',
        'abilities',
        'height',
        'weight',
        'base_experience',
        'gender',
        'egg_groups',
        'all_stats',
        'evolution_stage',
        'evolution_line',
        'normal_sprite',
        'animated_sprite',
        'data'
    )

    def __init__(
            self,
            pokemon,
            loop=asyncio.get_event_loop(),
            session=aiohttp.ClientSession()
    ):
        loop.create_task(self.__collect_data__())
        self.pokemon = pokemon
        self.session = session
        self.name = self.data.get('name')
        self.id = self.data.get('id')
        self.types = self.data.get('type')
        self.species = " ".join(self.data.get('species'))
        self.abilities = self.data.get('abilities')
        self.height = self.data.get('height')
        self.weight = self.data.get('weight')
        self.base_experience = int(self.data.get('base_experience'))
        self.gender = self.data.get('gender')
        self.egg_groups = self.data.get('egg_groups')
        self.all_stats = self.data.get('stats')
        self.evolution_stage = self.data.get('evolutionStage')
        self.evolution_line = self.data.get('evolutionLine')
        self.normal_sprite = self.data.get('sprites').get('normal')
        self.animated_sprite = self.data.get('sprites').get('animated')

    async def __collect_data__(self):
        data = await self.session.get('https://some-random-api.ml/pokedex?pokemon={0}'.format(self.pokemon))
        try:
            data = await data.json()
        except aiohttp.ContentTypeError:
            raise ValueError("Pokémon not found!")
        self.data = data

    def badge_mapping(self):
        return [TYPES.get(t.lower()) for t in self.types]

    def stat_mapping(self):
        return [f"**{STAT_NAMES.get(name.lower())}**: `{value}`" for name, value in self.all_stats.items()]





