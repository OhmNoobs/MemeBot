import random


def fortune_is_willing() -> bool:
    return bool(random.getrandbits(1))
