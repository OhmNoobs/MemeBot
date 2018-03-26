import random


def fortune_is_willing(percent=50) -> bool:
    return random.randrange(0, 100) < percent
