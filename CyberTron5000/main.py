"""
MIT License

Copyright (c) 2020 nizcomix

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import os

import asyncpg
import discord
from discord.ext import commands, tasks as t


def get_token():
    with open("json_files/secrets.json", "r") as f:
        res = json.load(f)
    return res


token = get_token()

print("INITIALISATION COMPLETE")
print("-----------------------")


class CyberTron5000(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix, pm_help=None, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False), case_insensitive=True, status=discord.Status.online)
        self.colour = 0x00dcff
        self.prefixes = {}
        self.ext = [f"CyberTron5000.cogs.{filename[:-3]}" for filename in os.listdir('cogs') if filename.endswith('.py')]
        self.load_extension(name='jishaku')
        self.loop.create_task(self.startup())
        self.loop.run_until_complete(self.create_db_pool())
        self.logging = dict(owner=350349365937700864,
                            logging_channel=727277234666078220,
                            invite='https://cybertron-5k.netlify.app/invite',
                            support='https://cybertron-5k.netlify.app/server',
                            github='https://github.com/niztg/CyberTron5000',
                            website='https://cybertron-5k.netlify.app',
                            reddit='https://reddit.com/r/CyberTron5000',
                            servers={
                                "CyberTron5000 Emotes 1": "https://discord.gg/29vqZfm",
                                "CyberTron5000 Emotes 2": "https://discord.gg/Qn7VYg8",
                                "CyberTron5000 Emotes 3": "https://discord.gg/Xgddz6W"
                            })

    async def create_db_pool(self):
        self.pg_con = await asyncpg.create_pool(user=token['psql_user'], password=token['psql_password'],
                                                database=token['psql_db'])

    async def get_prefix(self, message):
        if not message.guild:
            return 'c$'
        DEFAULT_PREFIX = ["c$"]
        prefixes = self.prefixes.get(message.guild.id, DEFAULT_PREFIX)
        return commands.when_mentioned_or(*prefixes)(self, message)

    def run(self, *args, **kwargs):
        super().run(token['bot_token'])

    @t.loop(minutes=3)
    async def loop(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                             name=f"{len(self.users):,} users in {len(self.guilds):,} guilds"))

    async def startup(self):
        await self.wait_until_ready()
        print(f"{self.user.name.upper()} IS ONLINE")
        print("-----------------------")
        for file in self.ext:
            try:
                self.load_extension(name=file)
            except Exception as error:
                print(f"Could not load {file}: {error}")
        print(f"COGS HAVE BEEN LOADED")
        print("-----------------------")
        prefix_data = await self.pg_con.fetch("SELECT guild_id, array_agg(prefix) FROM prefixes GROUP BY guild_id")
        for entry in prefix_data:
            self.prefixes[entry['guild_id']] = entry['array_agg']
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f"{len(self.users):,} users in {len(self.guilds):,} guilds"))
        print("PREFIXES AND PRESENCE SETUP")
        print("-----------------------")
        print("Ready!")


CyberTron5000().run()
