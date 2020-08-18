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

ALPHABET_NUMBER = {"A": 1,
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

INDICATOR_LETTERS = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣',
                     '9': '9️⃣', '0': '0️⃣'}

sl = {discord.Status.online: "<:online:726127263401246832>",
      discord.Status.offline: "<:offline:726127263203983440>",
      discord.Status.idle: "<:idle:726127192165187594>",
      discord.Status.dnd: "<:dnd:726127192001478746>"
      }

REDDIT_EMOJIS = {
    'Alpha Tester': '<:alphauser:742837407623151738>',
    'Bellwether': '<:bellwether:742837613228064912>',
    'Best Comment': '<:bestcomment:742837968179298355>',
    'Best Link': '<:bestlink:742838163990642809>',
    'ComboCommenter': '<:combocommenter:742838391078650017>',
    'ComboLinker': '<:combolinker:742838391229644900>',
    'Inciteful Comment': '<:incitefulcomment:742838606976122891>',
    'Inciteful Link': '<:incitefullink:742838454999711765>',
    'New User': '<:newuser:742838754841985164>',
    'Not Forgotten': '<:notforgotten:742838985251881091>',
    'Reddit Premium': '<:redditpremium:742839302840516860>',
    'RPAN Broadcaster': '<:rpanbroadcaster:742839517689413714>',
    'RPAN Viewer': '<:rpanviewer:742839518108844182>',
    'Sequence | Editor': '<:sequenceeditor:742839825165713468>',
    'Shutterbug': '<:shutterbug:742843728670097559>',
    'Verified Email': '<:verifiedemail:742843907099983873>',
    'Well-rounded': '<:wellrounded:742844034401173505>',
    'Xbox Live': '<:xboxlive:742844235216322651>',
    'Extra Life 2019': '<:extralife:742844662347333633>',
    'Open Sorcerer': '<:opensorcerer:742844988479766609>',
    'One-Year Club': '<:1_oneyear:742846966895083570>',
    'Two-Year Club': '<:1_twoyear:742846967213719592>',
    'Three-Year Club': '<:1_threeyear:742846966769123359>',
    'Four-Year Club': '<:1_fouryear:742846966735831132>',
    'Five-Year Club': '<:1_fiveyear:742846966794289212>',
    'Six-Year Club': '<:1_sixyear:742846966899277860>',
    'Seven-Year Club': '<:1_sevenyear:742846966979100803>',
    'Eight-Year Club': '<:1_eightyear:742846938264764476>',
    'Nine-Year Club': '<:1_nineyear:742846966630842399>',
    'Ten-Year Club': '<:1_tenyear:742846967071375468>',
    'Eleven-Year Club': '<:1_elevenyear:742846937992003616>',
    'Twelve-Year Club': '<:1_twelveyear:742846967033364480>',
    'Thirteen-Year Club': '<:1_thirteenyear:742846966689562625>',
    'Gilding I': '<:gilding1:742851900386443286>',
    'Gilding II': '<:gilding2:742851900545957990>',
    'Gilding III': '<:gilding3:742851900549890088>',
    'Gilding IV': '<:gilding4:742851938370060450>',
    'Gilding V': '<:gilding5:742852020490338355>',
    'Gilding VI': '<:gilding6:742852020808974487>',
    'Gilding VII': '<:gilding7:742852020855111781>',
    'Gilding VIII': '<:gilding9:742852020980940800>',
    'Gilding IX': '<:gilding9:742852020980940800>',
    'Gilding X': '<:gilding10:742852216963989646>',
    'Gilding XI': '<:gilding11:742852286044438648>'
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

engineer_bagdes = ["<:engineer1:732745844339638334>", "<:engineer2:732745844633370684>", "<:engineer3:732745844716994690>", "<:engineer4:732745844754743306>"]
popular_badges = ['<:popular1:732745781660090459>', '<:popular2:732745781856960634>', '<:popular3:732745782054092840>', '<:popular4:732745781714354198>']
legend_badges = ['<:legend1:732745816564826212>', '<:legend2:732745816590123041>', '<:legend3:73274581659838', '<:legend4:732745816758026381>']

ANIMALS = {
    'cat': '🐱',
    'dog': '🐶',
    'koala': '🐨',
    'fox': '🦊',
    'bird': '🐦',
    'birb': '🐦',
    'red_panda': '🔴',
    'elephant': '🐘',
    'panda': '🐼',
    'racoon': '🦝',
    'kangaroo': '🦘',
    'giraffe': '🦒',
    'whale': '🐋'
}