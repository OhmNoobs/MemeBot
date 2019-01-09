import typing

from pony.orm import Database, Set, PrimaryKey, db_session, Required, Optional

db = Database()


class User(db.Entity):
    id = PrimaryKey(int)
    is_bot = Required(bool)
    first_name = Required(str)
    last_name = Optional(str)
    username = Optional(str)
    language_code = Optional(str)
    wants_notifications = Required(bool)
    kudos_given = Set('User', reverse='kudos_received')
    kudos_received = Set('User', reverse='kudos_given')


def bind_db():
    db.bind(provider='sqlite', filename='neocortex.sqlite')
    db.generate_mapping()


def create_db():
    db.bind(provider='sqlite', filename='neocortex.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)


@db_session
def add_user(user_id: int, is_bot: bool, first_name: str, wants_notifications: bool,
             last_name: typing.Optional[str], username: typing.Optional[str],
             language_code: typing.Optional[str]) -> User:
    user = User(id=user_id, is_bot=is_bot, first_name=first_name, wants_notifications=wants_notifications,
                last_name=last_name, username=username, language_code=language_code)
    return user


@db_session
def get_user(user_id: int) -> User:
    return User[user_id]


@db_session
def give_kudos(giver: User, taker: User) -> None:
    giver.kudos_given.add(taker)


@db_session
def toggle_wants_notification(user: User) -> None:
    user.wants_notifications = not user.wants_notifications


if __name__ == '__main__':

    # create_db()

    with db_session:
        a = User(id=1, is_bot=False, first_name='Hans', wants_notifications=True)
        b = User(id=2, is_bot=False, first_name='Erich', wants_notifications=False)
        a.kudos_given.add(b)
        print(User[1].kudos_received)
        print(User[1].kudos_given)
        print(User[2].kudos_received)
