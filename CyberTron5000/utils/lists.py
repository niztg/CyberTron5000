"""

For JSON lists.

"""

import discord

STAT_NAMES = {
    "speed": "SPEED",
    "attack": "ATTACK",
    "sp_atk": "SPECIAL ATTACK",
    "sp_def": "SPECIAL DEFENSE",
    "defense": "DEFENSE",
    "hp": "HP",
    "total": "TOTAL"
    
}

ALPHABET_NUMBER = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
    "K": 11,
    "L": 12,
    "M": 13,
    "N": 14,
    "O": 15,
    "P": 16,
    "Q": 17,
    "R": 18,
    "S": 19,
    "T": 20,
    "U": 21,
    "V": 22,
    "W": 23,
    "X": 24,
    "Y": 25,
    "Z": 26
}
NUMBER_ALPHABET = {value: key for (key, value) in ALPHABET_NUMBER.items()}

TYPES = {
    "normal": "<:normal:715628305541496915>",
    "fighting": "<:fighting:715628306015191220>",
    "fire": "<:fire:715626721402945567>",
    "water": "<:water:715629330621005915>",
    "grass": "<:grass:715629330830721104>",
    "ground": "<:ground:715626721772175472>",
    "rock": "<:rock:715626723126804532>",
    "steel": "<:steel:715629330637520988>",
    "fairy": "<:fairy:715629865071542328>",
    "ghost": "<:ghost:715630366769021038>",
    "dark": "<:dark:715630366651711549>",
    "poison": "<:poison:715628305671389285>",
    "dragon": " <:dragon:715630390597124177>",
    "electric": "<:electric:715626721399013489>",
    "ice": "<:ice:715630367687573774>",
    "flying": "<:flying:715631197140811847>",
    "bug": "<:bug:715627787427381319>",
    "psychic": "<:psychic:715628305763663923>"
}

REGIONS = {
    "europe": "Europe",
    "us-east": "US East",
    "india": "India",
    "brazil": "Brazil",
    "japan": "Japan",
    "russia": "Russia",
    "singapore": "Singapore",
    "southafrica": "South Africa",
    "sydney": "Sydney",
    "hongkong": "Hong Kong",
    "us-central": "US Central",
    "us-south": "US South",
    "us-west": "US West",
    'eu-west': "EU West",
    "eu-north": "EU North",
    "eu-south": "EU South",
    "eu-east": "EU East"
}

INDICATOR_LETTERS = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣',
                     '4': '4️⃣', '5': '5️⃣', '6': '6️⃣',
                     '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'}

sl = {
    discord.Status.online: "<:online:726127263401246832>",
    discord.Status.offline: "<:offline:726127263203983440>",
    discord.Status.idle: "<:idle:726127192165187594>",
    discord.Status.dnd: "<:dnd:726127192001478746>"
}

emotes = {
    'eight-year club': '<:eightyearclub:702188391961198683>',
    'alpha tester': '<:alpha_user:702188392154267715>',
    'best comment': '<:bestcomment:702188392175370240>',
    'combocommenter': '<:combocommenter:702188392183758910>',
    'bellwether': '<:bellwether:702188392192147546>',
    'combolinker': '<:combolinker:702188392196341940>',
    'best link': '<:bestlink:702188392221507654>',
    'eleven-year club': '<:elevenyearclub:702188392384954459>',
    'four-year club': '<:fouryearclub:702188392489943251>',
    'extra life': '<:extralife:702188392506458212>',
    'gilding iii': '<:gildingiii:702188392590344264>',
    'gilding vii': '<:gildingvii:702188392607383564>',
    'gilding v': '<:gildingv:702188392645001277>',
    'gilding ii': '<:gildingii:702188392657715312>',
    'five-year club': '<:fiveyearclub:702188392779087942>',
    'gilding iv': '<:gildingiv:702188392808448080>',
    'gilding vi': '<:gildingvi:702188392842133505>',
    'gilding i': '<:gildingi:702188392842133545>',
    'gilding ix': '<:gildingix:702188392867430480>',
    'gilding viii': '<:gildingviii:702188392917630986>',
    'gilding x': '<:gildingx:702188394108682241>',
    'rpan viewer': '<:rpanviewer:702188394226384997>',
    'inciteful link': '<:incitefullink:702188394373185666>',
    'one-year club': '<:oneyearclub:702188394398220290>',
    'not_forgotten': '<:not_forgotten:702188394402283541>',
    'new user': '<:newuser:702188394423386263>',
    'gilding xi': '<:gildingxi:702188394427580427>',
    'inciteful comment': '<:incitefulcomment:702188394440163378>',
    'nine-year club': '<:nineyearclub:702188394490363945>',
    'open sorcerer': '<:opensorcerer:702188394490626150>',
    'two-year club': '<:twoyearclub:702188394519986248>',
    'reddit_gold': '<:reddit_gold:702188394616193125>',
    'undead | lich': '<:undeadlich:702188394624843887>',
    'undead | zombie': '<:undeadzombie:702188394649878561>',
    'sequence | editor': '<:sequence_editor:702188394729570364>',
    'sequence | screenwriter': '<:sequence_text:702188394851074500>',
    'seven-year club': '<:sevenyearclub:702188394851205200>',
    'six-year club': '<:sixyearclub:702188394863656960>',
    'three-year club': '<:threeyearclub:702188394872176680>',
    'ten-year club': '<:tenyearclub:702188394914119720>',
    'shutterbug': '<:shutterbug:702188394918445166>',
    'verified email': '<:verifiedemailaddress:702188394930765835>',
    'xboxl live': '<:xboxlive:702188394930765845>',
    'thirteen-year club': '<:thirteenyearclub:702188394947543060>',
    'rpan broadcaster': '<:rpanbroadcaster:702188394947674213>',
    'twelve-year club': '<:twelveyearclub:702188394956062740>',
    'undead | necromancer': '<:undeadnecromancer:702188395111383130>',
    'well-rounded': '<:wellrounded:702188395136548874>',
    'spared': '<:thanos_spared:702219317021769759>',
    'secret santa': '<:ss:702219316938014750>',
    'redditgifts elf': '<:elf:702219316694745110>',
    'not forgotten': '<:not_forgotten:702219317143404675>',
    'reddit premium': '<:reddit_gold:702219317051129906>',
    'redditgifts exchanges': '<:rgexchange:702219316875231273>'
}

status_mapping = {
    discord.ActivityType.listening: "Listening to",
    discord.ActivityType.watching: "Watching",
    discord.ActivityType.playing: "Playing",
    discord.ActivityType.streaming: "Streaming",
    discord.ActivityType.custom: "\u200b"
}

badge_mapping = {
    "staff": "<:staff:730846674775179394>",
    "partner": "<:partner:730846624275759105>",
    "hypesquad": "<:hypesquad:730846721235746859>",
    "bug_hunter": "<:bug_hunter:730868709274419281>",
    "bug_hunter_level_2": "<:bug_hunter_level_2:730874021721276527>",
    "hypesquad_bravery": "<:hypesquad_bravery:730851606941270147>",
    "hypesquad_brilliance": "<:hypesquad_brilliance:730851606853320765>",
    "hypesquad_balance": "<:hypesquad_balance:730851606832087141>",
    "early_supporter": "<:early_supporter:730869784337580102>",
    "verified_bot_developer": "<:verified_bot_developer:730849897410199572>",
}
audit_actions = {
    discord.AuditLogAction.guild_update: "**updated the guild**",
    discord.AuditLogAction.channel_update: "**updated channel**",
    discord.AuditLogAction.channel_create: "**created channel**",
    discord.AuditLogAction.channel_delete: "**deleted channel**",
    discord.AuditLogAction.overwrite_create: "**created overwrite**",
    discord.AuditLogAction.overwrite_update: "**updated overwrite**",
    discord.AuditLogAction.overwrite_delete: "**deleted overwrite**",
    discord.AuditLogAction.kick: "**kicked**",
    discord.AuditLogAction.ban: "**banned**",
    discord.AuditLogAction.unban: "**unbanned**",
    discord.AuditLogAction.member_role_update: "**updated roles of**",
    discord.AuditLogAction.member_move: "**moved member**",
    discord.AuditLogAction.member_disconnect: "**disconnected member**",
    discord.AuditLogAction.bot_add: "**added bot**",
    discord.AuditLogAction.role_create: "**created role**",
    discord.AuditLogAction.role_update: "**updated role**",
    discord.AuditLogAction.role_delete: "**deleted role**",
    discord.AuditLogAction.invite_create: "**created invite**",
    discord.AuditLogAction.invite_update: "**updated invite**",
    discord.AuditLogAction.invite_delete: "**deleted invite**",
    discord.AuditLogAction.webhook_create: "**created webhook**",
    discord.AuditLogAction.webhook_delete: "**deleted webhook**",
    discord.AuditLogAction.webhook_update: "**updated webhook**",
    discord.AuditLogAction.emoji_create: "**created emoji**",
    discord.AuditLogAction.emoji_update: "**updated emoji**",
    discord.AuditLogAction.emoji_delete: "**deleted emoji**",
    discord.AuditLogAction.message_delete: "**deleted message by**",
    discord.AuditLogAction.message_pin: "**pinned a message by**",
    discord.AuditLogAction.message_unpin: "**unpinned a message by**",
    discord.AuditLogAction.message_bulk_delete: "**bulk deleted messages**",
    discord.AuditLogAction.integration_create: "**created integration**",
    discord.AuditLogAction.integration_delete: "**deleted integration**",
    discord.AuditLogAction.integration_update: "**updated integration**",
    discord.AuditLogAction.member_update: "**updated member**"
}

engineer_bagdes = ["<:engineer1:732745844339638334>",
                   "<:engineer2:732745844633370684>",
                   "<:engineer3:732745844716994690>",
                   "<:engineer4:732745844754743306>"]

popular_badges = ['<:popular1:732745781660090459>'
    , '<:popular2:732745781856960634>'
    , '<:popular3:732745782054092840>'
    , '<:popular4:732745781714354198>']

legend_badges = ['<:legend1:732745816564826212>',
                 '<:legend2:732745816590123041>',
                 '<:legend3:732745816598380636>',
                 '<:legend4:732745816758026381>']
