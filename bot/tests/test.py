import random

from common import ROOT_DIR
from pathlib import Path

from telegram import User

PATH_TO_RESOURCES = Path(ROOT_DIR) / "tests" / "resources"


def random_id():
    return random.randint(1, 1337)


def mock_telegram_user(name):
    return User(id=random_id(), first_name=name, is_bot=False, username=name)
