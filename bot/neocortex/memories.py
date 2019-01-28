import re
import typing
from datetime import datetime
from typing import Iterator

import telegram
from pony.orm import db_session, desc
from neocortex import log, User, Kudos

username_validator = re.compile(r"([a-zA-Z0-9_]){5,32}")


class TopKudosReceiver(typing.NamedTuple):
    name: str
    kudos_received: int


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
        name = user.username if user.username else user.first_name
        top_receivers.append(TopKudosReceiver(name, len(user.kudos_received)))
    return top_receivers


@db_session
def _add_user(username: str) -> User:
    if valid_username(username):
        log.info(f'User({username}) unknown. Adding him now.')
        user = User(username=username)
        return user
    else:
        error = f"Invalid telegram username provided '{username}' does not comply with telegrams username policies."
        log.error(error)
        raise TypeError(error)


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
    giver = User[giver.internal_id]  # type: User
    taker = User[taker.internal_id]  # type: User
    log.info(f"{giver.username} gave kudos to {taker.username}")
    Kudos(giver=giver, taker=taker, timestamp=datetime.now())


@db_session
def get_kudos_of_user(user: User):
    return len(User[user.internal_id].kudos_received)


def _to_telegram_user(user: User) -> telegram.User:
    subscriber = user.to_dict()
    subscriber["id"] = subscriber.pop("telegram_id")
    return telegram.User(**subscriber)


def valid_username(username):
    """
    According to https://core.telegram.org/method/account.checkUsername:
    Accepted characters: A-z (case-insensitive), 0-9 and underscores. Length: 5-32 characters.
    """
    return len(username_validator.findall(username)) == 1

