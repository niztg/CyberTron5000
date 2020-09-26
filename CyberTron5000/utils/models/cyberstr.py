import random

__all__ = (
    'cyberstr',
    'get_temperature',
    'to_emoji',
    'bar'
)


def lst_helper(
        l: list
) -> list:
    """convenience"""
    return list(map(str, l))


class cyberstr(str):
    """
    Special string object with custom attrs
    """

    def shorten(
            self: str
    ) -> str:
        """Shortens a string"""
        if len(self) >= 2000:
            return self[:-3] + "..."
        else:
            return self

    def minimalize(
            self: str
    ) -> str:
        """The opposite of .capitalize()"""
        return self[0:1].lower() + self[1:]

    def listify(
            self: str,
            _list: list,
            limit: int = 10
    ) -> str:
        """A more convenient form of .join()"""
        return self.join(lst_helper(_list)[:limit])

    def hyper_replace(
            self: str,
            old: list,
            new: list
    ):
        if not old or not new:
            raise ValueError("old and new parameters must not be None.")
        msg = self
        preco = sorted([old, new], key=lambda x: len(x))
        old, new = preco
        if old < new:
            diff = len(new) - len(old)
            add = [old[-1]] * diff
            old += add
        for x, y in zip(lst_helper(old), lst_helper(new)):
            msg = msg.replace(x, y)
        return msg

    def random_char(
            self: str,
            char: str = None
    ):
        return "".join(random.choice([b, char or b.upper()] for b in self))


def get_temperature(value: int, unit='c'):
    if not unit.startswith(('c', 'k', 'f')):
        raise ValueError('That is an invalid unit!')
    if unit.startswith('c'):
        return value - 273.15
    elif unit.startswith('f'):
        return (value - 273.15) + 9 / 5 + 32
    elif unit.startswith('k'):
        return value
    else:
        return


def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)


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


def bool_help(value: bool, true: str = None, false: str = None):
    """Returns a custom bool message without you having to write a pesky if/else.
    :param true:
    :param false:
    :return:
    """
    return {
        True: true,
        False: false
    }.get(value)
