"""

For JSON lists.

"""
# I need to use yaml for all of this
# excuse me

from string import ascii_uppercase

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

ALPHABET_NUMBER = {letter: number for (letter, number) in zip(ascii_uppercase, list(range(1, 27)))}

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

engineer_bagdes = ["<:engineer1:732745844339638334>", "<:engineer2:732745844633370684>",
                   "<:engineer3:732745844716994690>", "<:engineer4:732745844754743306>"]
popular_badges = ['<:popular1:732745781660090459>', '<:popular2:732745781856960634>', '<:popular3:732745782054092840>',
                  '<:popular4:732745781714354198>']
legend_badges = ['<:legend1:732745816564826212>', '<:legend2:732745816590123041>', '<:legend3:73274581659838',
                 '<:legend4:732745816758026381>']

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

EMOTIONS = {
    'hug': '<a:hug:748315930685210746>',
    'wink': '😉',
    'face-palm': '🤦‍♂️',
    'pat': '<:pat:748316152123359322>'
}

INFRACTION_DESCRIPTIONS = {
    "mute": "This will indefinitely mute the user by addding to them the `CyberMute` role, which restricts them from seeing any channels. To unmute them, manually remove the role from them or do `{0}unumute <user>`\nI need **Manage Channels** and **Manage Roles** permissions for this.",
    "kick": "This will kick the user from the server.\nI need the **Kick Members** permission for this.",
    "ban": "This will ban the user from the server. To unban a user, do `{0}unban <user id or username#user discriminator>`"
}

WEAPONS = [
    "Sword of Mega Doom",
    "Epic Gun",
    "Mega Epic Gun",
    "Grenade",
    "Amazing Bruh Machine",
    "Gun Lmao",
    "Hyper Epic Gun",
    "'Not even trying at this point' Rifle",
    "Grand Sword of Chaos",
    "Excalibur",
    "Master Sword",
    "Storm Pegasus",
    "Rock Leone",
    "Lightning L-Drago"
]

QUIPS = ["What two words would passengers never want to hear a pilot say?",
         "You would never go on a roller coaster called _____",
         "The secret to a happy life",
         "If a winning coach gets Gatorade dumped on his head, what should get dumped on the losing coach?",
         "Name a candle scent designed specifically for Kim Kardashian",
         "You should never give alcohol to ______",
         "Everyone knows that monkeys hate ______",
         "The biggest downside to living in Hell",
         "Jesus's REAL last words",
         "The worst thing for an evil witch to turn you into",
         "The Skittles flavor that just missed the cut",
         "On your wedding night, it would be horrible to find out that the person you married is ____",
         "A name for a really bad Broadway musical",
         "The first thing you would do after winning the lottery",
         "Why ducks really fly south in the winter",
         "America's energy crisis would be over if we made cars that ran on ______",
         "It's incredibly rude to ____ with your mouth open",
         "What's actually causing global warming?",
         "A name for a brand of designer adult diapers",
         "Name a TV drama that's about a vampire doctor",
         "Something squirrels probably do when no one is looking",
         "The crime you would commit if you could get away with it",
         "What's the Mona Lisa smiling about?",
         "A terrible name for a cruise ship",
         "What FDR meant to say was We have nothing to fear, but _____",
         "Come up with a title for an adult version of any classic video game",
         "The name of a font nobody would ever use",
         "Something you should never put on an open wound",
         "Scientists say erosion, but we all know the Grand Canyon was actually made by _____",
         "The real reason the dinosaurs died",
         "Come up with the name of a country that doesn't exist",
         "The best way to keep warm on a cold winter night",
         "A college major you don't see at many universities",
         "What would make baseball more entertaining to watch?",
         "The best thing about going to prison",
         "The best title for a new national anthem for the USA",
         "Come up with the name of book that would sell a million copies, immediately",
         "What would you do if you were left alone in the White House for an hour?",
         "Invent a family-friendly replacement word that you could say instead of an actual curse word",
         "The name of the reindeer Santa didn't pick to pull his sleigh",
         "What's the first thing you would do if you could time travel?",
         "The name of a pizza place you should never order from",
         "A not-very-scary name for a pirate",
         "Come up with a name for a beer made especially for monkeys",
         "The best thing about living in an igloo",
         "The worst way to be murdered",
         "Something you shouldn't get your significant other for Valentine's Day",
         "A dangerous thing to do while driving",
         "Something you shouldn't wear to a job interview",
         "The #1 reason penguins can't fly",
         "Using only two words, a new state motto for Texas",
         "The hardest thing about being Batman",
         "A great way to kill time at work",
         "Come up with a really bad TV show that starts with Baby",
         "Why does the Tower of Pisa lean?",
         "What's wrong with these kids today?",
         "A great new invention that starts with Automatic",
         "Come up with a really bad football penalty that begins with Intentional",
         "A Starbucks coffee that should never exist",
         "There's Gryffindor, Ravenclaw, Slytherin, and Hufflepuff, but what's the Hogwarts house few ",
         "have ever heard of?",
         "The worst words to say for the opening of a eulogy at a funeral",
         "Something you should never use as a scarf",
         "Invent a holiday that you think everyone would enjoy",
         "The best news you could get today",
         "Usually, it's bacon,lettuce and tomato, but come up with a BLT you wouldn't want to eat",
         "The worst thing you could stuff a bed mattress with",
         "A great opening line to start a conversation with a stranger at a party",
         "Something you would like to fill a swimming pool with",
         "Miley Cyrus' Wi-Fi password, possibly",
         "If you were allowed to name someone else's baby any weird thing you wanted, ",
         "what would you name it?",
         "A fun thing to think about during mediocre sex",
         "You know you're in for a bad taxi ride when _____",
         "Where do babies come from?",
         "The terrible fate of the snowman Olaf in a director's cut of 'Frozen'",
         "Sometimes, after a long day, you just need to ______",
         "The worst way to spell Mississippi",
         "Give me one good reason why I shouldn't spank you right now",
         "The best pick-up line for an elderly singles mixer",
         "A good stage name for a chimpanzee stripper",
         "The best place to bury all those bodies",
         "One place a finger shouldn't go",
         "Come up with a name for the most difficult yoga pose known to mankind",
         "What's lurking under your bed when you sleep?",
         "The name of a canine comedy club with puppy stand-up comedians",
         "A great name for a nude beach in Alaska",
         "Make up the title of a movie that is based on the first time you had sex",
         "A vanity license plate a jerk in an expensive car would get",
         "A good fake name to use when checking into a hotel",
         "A good catchphrase to yell every time you finish pooping",
         "Your personal catchphrase if you were on one of those 'Real Housewives' shows",
         "The Katy Perry Super Bowl halftime show would have been better with _____",
         "Okay... fine! What do YOU want to talk about then?!!!",
         "Miller Lite beer would make a lot of money if they came up with a beer called Miller Lite _____",
         "Something you should never stick up your butt",
         "A terrible name for a clown",
         "An inappropriate thing to do at a cemetery"]
