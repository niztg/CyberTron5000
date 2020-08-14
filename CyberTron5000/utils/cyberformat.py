"""
bruh
"""

import random

import discord


def shorten(s: str):
    if len(s) >= 2000:
        return s[:-3] + "..."
    else:
        return s


def minimalize(string):
    final = ''
    final += string[0:1].lower() + string[1:] if string else ''
    return final


def listify(list: list, char='\n', limit: int = None):
    """
    Puts everything in a pretty list for you.

    :param list:
    :param char:
    :param limit:
    :return:
    """
    if not limit:
        return f"{char}".join(list)
    else:
        return f"{char}".join(list[:limit])


def hyper_replace(text, old: list, new: list):
    """
    Allows you to replace everything you need in one function using two lists.
    :param text:
    :param old:
    :param new:
    :return:
    """
    msg = str(text)
    for x, y in zip(old, new):
        msg = str(msg).replace(x, y)
    return msg


def bool_help(value: bool, true: str = None, false: str = None):
    """Returns a custom bool message without you having to write a pesky if/else.
    :param true:
    :param false:
    :return:
    """
    if value:
        return true
    else:
        return false


def bar(stat: int, max: int, filled: str, empty: str, pointer: bool = False, show_stat: bool = None):
    if not pointer:
        percent = round((stat / max) * 100, 1)
        if percent > 100:
            bar = f"{percent}% {filled * 10} 100.0%" if not show_stat else f"{filled * 10}"
            return bar
        elif percent <= 0:
            bar = f"{percent}% {empty * 10} 100.0%" if not show_stat else f"{empty * 10}"
            return bar
        elif 0 < percent < 5:
            return f"{str(percent)}% {filled * 1}{empty * 9} 100.0%" if not show_stat else f"{filled * 1}{empty * 9}"
        else:
            total_filled = round(percent / 10)
            total_empty = 10 - (round(percent / 10))
            return f"{str(percent)}% {filled * total_filled}{empty * total_empty} 100.0%" if not show_stat else f"{filled * total_filled}{empty * total_empty}"
    elif pointer:
        percent = round((stat / max) * 100, 1)
        if percent > 100:
            bar = f"{percent}% {filled * 9}{empty} 100.0%" if not show_stat else f"{filled * 9}{empty}"
            return bar
        elif percent <= 0:
            bar = f"{percent}% {filled * 10} 100.0%" if not show_stat else f"{filled * 10}"
            return bar
        elif 0 <= percent <= 5:
            return f"{str(percent)}% {empty * 1}{filled * 9} 100.0%" if not show_stat else f"{filled * 1}{empty * 9}"
        else:
            total_filled = round(percent / 10)
            total_empty = 10 - (round(percent / 10))
            return f"{str(percent)}% {filled * (total_filled - 1)}{empty}{filled * total_empty} 100.0%" if not show_stat else f"{filled * (total_filled - 1)}{empty}{filled * total_empty}"


def fieldify(embed: discord.Embed, names: list, values: list, inline: bool = True, limit: int = None):
    """Easy embed fieldification
        :returns embed:
        """
    embed = embed
    if not limit:
        for name, val in zip(names, values):
            embed.add_field(name=name, value=val, inline=inline)

    elif limit:
        counter = 0
        for name, val in zip(names, values):
            embed.add_field(name=name, value=val, inline=inline)
            counter += 1
            if counter >= limit:
                return embed
            else:
                continue
    return embed


def codeblock(body, lang: str = 'py'):
    if str(body).startswith(f"```{lang}") and str(body).endswith("```"):
        py, c = str(body).split(f"```{lang}")
        return c[:-3]
    else:
        return body


def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)


def better_random_char(s: str, c: str = None):
    return "".join(random.choice([b, c or b.upper()]) for b in s)


def get_temperature(value: int, unit='c'):
    if not unit.startswith(('c', 'k', 'f')):
        raise ValueError('That is an invalid unit!')
    if unit.startswith('c'):
        return value - 273.15
    elif unit.startswith('f'):
        return (value - 273.15) + 9/5 + 32
    elif unit.startswith('k'):
        return value
    else:
        return
