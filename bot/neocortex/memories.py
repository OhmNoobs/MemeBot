import logging
import typing
from datetime import datetime
from typing import Iterator
import re

import telegram
from pony.orm import Database, Set, db_session, Required, Optional, PrimaryKey

DB_FILE = 'neocortex.sqlite'
db = Database()
log = logging.getLogger()
username_validator = re.compile(r"([a-zA-Z0-9_]){5,32}")


class User(db.Entity):
    internal_id = PrimaryKey(int, auto=True)
    telegram_id = Optional(int, unique=True)  # nullable=True
    username = Optional(str, unique=True, nullable=True)
    is_bot = Optional(bool)  # nullable=True
    first_name = Optional(str, nullable=True)
    last_name = Optional(str, nullable=True)
    language_code = Optional(str, nullable=True)
    wants_notifications = Optional(bool)  # nullable=True
    kudos_given = Set('Kudos', reverse='giver')
    kudos_received = Set('Kudos', reverse='taker')


class Kudos(db.Entity):
    id = PrimaryKey(int, auto=True)
    giver = Required(User, reverse='kudos_given')
    taker = Required(User, reverse='kudos_received')
    timestamp = Required(datetime)


def bind_db():
    db.bind(provider='sqlite', filename=DB_FILE)
    db.generate_mapping()


def create_db():
    db.bind(provider='sqlite', filename=DB_FILE, create_db=True)
    db.generate_mapping(create_tables=True)


@db_session
def add_telegram_user(user: telegram.User) -> User:
    user = User(telegram_id=user.id, is_bot=user.is_bot, first_name=user.first_name, last_name=user.last_name,
                username=user.username, language_code=user.language_code)
    return user


@db_session
def add_user(username: str) -> User:
    validate_username(username)
    user = User(username=username)
    return user


def validate_username(username):
    """
    According to https://core.telegram.org/method/account.checkUsername:
    Accepted characters: A-z (case-insensitive), 0-9 and underscores. Length: 5-32 characters.
    """
    if len(username_validator.findall(username)) != 1:
        raise ValueError("Invalid telegram username provided.")
    pass


@db_session
def get_user(telegram_id: int) -> typing.Optional[User]:
    return User.get(telegram_id=telegram_id)


@db_session
def remember_telegram_user(user: telegram.User) -> User:
    user = get_user(user.id)
    if not user:
        log.info(f'User {user.first_name} unknown. Adding him now.')
        user = add_telegram_user(user)
    return user


@db_session
def remember_username(username: str) -> User:
    user = get_user_by_username(username)
    if not user:
        log.info(f'Username ({username}) unknown. Adding him now.')
        user = add_user(username)
    return user


@db_session
def get_user_by_username(username: str) -> typing.Optional[User]:
    username = username.lower()
    return User.get(lambda user: user.username.lower() == username)


@db_session
def give_kudos(giver: User, taker: User) -> None:
    giver = User[giver.internal_id]
    taker = User[taker.internal_id]
    Kudos(giver=giver, taker=taker, timestamp=datetime.now())


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
    return map(to_telegram_user, subscribers)


def to_telegram_user(user: User) -> telegram.User:
    subscriber = user.to_dict()
    subscriber["id"] = subscriber.pop("telegram_id")
    return telegram.User(**subscriber)


if __name__ == '__main__':
    create_db()
