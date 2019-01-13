import logging
import re
import typing
from datetime import datetime
from pathlib import Path
from typing import Iterator

import telegram
from pony.orm import Database, Set, db_session, Required, Optional, PrimaryKey, desc

DB_FILE = Path('neocortex.sqlite')
db = Database()
log = logging.getLogger()
username_validator = re.compile(r"([a-zA-Z0-9_]){5,32}")


class User(db.Entity):
    internal_id = PrimaryKey(int, auto=True)
    telegram_id = Optional(int, unique=True)
    username = Optional(str, unique=True, nullable=True)
    is_bot = Optional(bool)
    first_name = Optional(str, nullable=True)
    last_name = Optional(str, nullable=True)
    language_code = Optional(str, nullable=True)
    wants_notifications = Optional(bool)
    kudos_given = Set('Kudos', reverse='giver')
    kudos_received = Set('Kudos', reverse='taker')


class Kudos(db.Entity):
    id = PrimaryKey(int, auto=True)
    giver = Required(User, reverse='kudos_given')
    taker = Required(User, reverse='kudos_received')
    timestamp = Required(datetime)


class TopKudosReceiver(typing.NamedTuple):
    name: str
    kudos_received: int


def bind_db():
    if DB_FILE.is_file():
        db.bind(provider='sqlite', filename=DB_FILE.name)
        db.generate_mapping()
    else:
        log.info("Database file doesn't exist. Creating...")
        create_db()


def create_db():
    db.bind(provider='sqlite', filename=DB_FILE.name, create_db=True)
    db.generate_mapping(create_tables=True)


@db_session
def remember_telegram_user(user: telegram.User) -> User:
    rich_user_memory = _get_user(user.id)
    if not rich_user_memory:
        rich_user_memory = _create_or_update(user)
    return rich_user_memory


@db_session
def remember_username(username: str) -> User:
    user = _get_user_by_username(username)
    if not user:
        user = _add_user(username)
    return user


@db_session
def toggle_wants_notification(remembered_user: User) -> None:
    user = User[remembered_user.internal_id]
    if not user.wants_notifications:
        user.wants_notifications = True
    else:
        user.wants_notifications = False


@db_session
def get_subscribers() -> Iterator[telegram.User]:
    subscribers = list(User.select(lambda user: user.wants_notifications))
    return map(_to_telegram_user, subscribers)


@db_session
def remember_top_n_kudos_receivers(n: int) -> typing.List[TopKudosReceiver]:
    top_n = User.select().order_by(lambda user: desc(len(user.kudos_received)))
    top_n = top_n.filter(lambda user: len(user.kudos_received) > 0)[:n]
    top_receivers = []
    for user in top_n:
        name = f'@{user.username}' if user.username else user.first_name
        top_receivers.append(TopKudosReceiver(name, len(user.kudos_received)))
    return top_receivers


@db_session
def _add_user(username: str) -> User:
    validate_username(username)
    log.info(f'User({username}) unknown. Adding him now.')
    user = User(username=username)
    return user


@db_session
def _add_telegram_user(user: telegram.User) -> User:
    log.info(f'Adding user {user.name}.')
    user = User(telegram_id=user.id, is_bot=user.is_bot, first_name=user.first_name, last_name=user.last_name,
                username=user.username, language_code=user.language_code)
    return user


@db_session
def _get_user(telegram_id: int) -> typing.Optional[User]:
    return User.get(telegram_id=telegram_id)


@db_session
def _create_or_update(user: telegram.User):
    if _get_user_by_username(user.username):
        remembered_telegram_user = _update_username_only_user_to_telegram_user(user)
    else:
        remembered_telegram_user = _add_telegram_user(user)
    return remembered_telegram_user


@db_session
def _update_username_only_user_to_telegram_user(user: telegram.User) -> User:
    user_memory = _get_user_by_username(user.username)
    new_user_information = _prepare_for_update(user)
    user_memory.set(**new_user_information)
    log.info(f"Updated information about User {user.full_name} (was previously only known as {user.username})")
    return user_memory


def _prepare_for_update(user):
    new_user_information = user.to_dict()
    new_user_information["telegram_id"] = new_user_information.pop("id")
    return new_user_information


@db_session
def _get_user_by_username(username: str) -> typing.Optional[User]:
    username = username.lower()
    return User.get(lambda user: user.username.lower() == username)


@db_session
def give_kudos(giver: User, taker: User) -> None:
    giver = User[giver.internal_id]
    taker = User[taker.internal_id]
    Kudos(giver=giver, taker=taker, timestamp=datetime.now())


def _to_telegram_user(user: User) -> telegram.User:
    subscriber = user.to_dict()
    subscriber["id"] = subscriber.pop("telegram_id")
    return telegram.User(**subscriber)


def validate_username(username):
    """
    According to https://core.telegram.org/method/account.checkUsername:
    Accepted characters: A-z (case-insensitive), 0-9 and underscores. Length: 5-32 characters.
    """
    if len(username_validator.findall(username)) != 1:
        raise ValueError("Invalid telegram username provided.")
    pass


if __name__ == '__main__':
    create_db()
