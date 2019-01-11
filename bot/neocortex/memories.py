from typing import Iterator

import telegram
from pony.orm import Database, Set, db_session, Required, Optional, PrimaryKey

DB_FILE = 'neocortex.sqlite'
db = Database()


class User(db.Entity):
    internal_id = PrimaryKey(int, auto=True)
    telegram_id = Optional(int, unique=True, nullable=True)
    username = Optional(str, unique=True, nullable=True)
    is_bot = Optional(bool, nullable=True)
    first_name = Optional(str, nullable=True)
    last_name = Optional(str, nullable=True)
    language_code = Optional(str, nullable=True)
    wants_notifications = Required(bool)
    kudos_given = Set('User', reverse='kudos_received')
    kudos_received = Set('User', reverse='kudos_given')


def bind_db():
    db.bind(provider='sqlite', filename=DB_FILE)
    db.generate_mapping()


def create_db():
    db.bind(provider='sqlite', filename=DB_FILE, create_db=True)
    db.generate_mapping(create_tables=True)


@db_session
def add_user(user: telegram.User, wants_notifications=False) -> User:
    user = User(telegram_id=user.id, is_bot=user.is_bot, first_name=user.first_name,
                wants_notifications=wants_notifications, last_name=user.last_name, username=user.username,
                language_code=user.language_code)
    return user


@db_session
def get_user(telegram_id: int) -> User:
    return User.get(telegram_id=telegram_id)


@db_session
def give_kudos(giver: User, taker: User) -> None:
    giver.kudos_given.add(taker)


@db_session
def toggle_wants_notification(remembered_user: User) -> None:
    user = User[remembered_user.internal_id]
    user.wants_notifications = not user.wants_notifications


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
    # bind_db()

    with db_session:
        # a = User(id=1, is_bot=False, first_name='Hans', wants_notifications=True)
        # b = User(id=2, is_bot=False, first_name='Erich', wants_notifications=False)
        # a.kudos_given.add(b)
        # print(User[1].kudos_received)
        # print(User[1].kudos_given)
        # print(User[2].kudos_received)
        pass
