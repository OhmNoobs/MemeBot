from datetime import datetime
import logging
import os
from pathlib import Path

from pony.orm import Database, PrimaryKey, Optional, Set, Required

_DB_FILE_LOCATION = Path(os.path.abspath(__file__)).parent / 'neocortex.sqlite'
db = Database()
log = logging.getLogger()


def bind_db(db_path: Path = _DB_FILE_LOCATION):
    if _DB_FILE_LOCATION.is_file():
        db.bind(provider='sqlite', filename=db_path.name)
        db.generate_mapping()
    else:
        log.info("Database file doesn't exist. Creating...")
        create_db(db_path.name)


def create_db(filename: str):
    db.bind(provider='sqlite', filename=filename, create_db=True)
    db.generate_mapping(create_tables=True)


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
    transactions_sent = Set('Transaction', reverse='sender')
    transactions_received = Set('Transaction', reverse='receiver')
    balance = Optional(float, default=0)
    banned_until = Optional(datetime)
    groups = Set('Group')


class Kudos(db.Entity):
    id = PrimaryKey(int, auto=True)
    giver = Required(User, reverse='kudos_given')
    taker = Required(User, reverse='kudos_received')
    timestamp = Required(datetime)


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    price = Required(float)
    for_sale = Required(bool)
    description = Optional(str, nullable=True)
    image_path = Optional(str, nullable=True)
    transactions = Set('Transaction')


class Transaction(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Required(float)
    timestamp = Required(datetime)
    description = Optional(str, 2000, nullable=True, lazy=True)
    sender = Required(User, reverse='transactions_sent')
    receiver = Required(User, reverse='transactions_received')
    product = Optional(Product)


class Group(db.Entity):
    id = Required(int)
    name = Required(str)
    members = Set(User)
    PrimaryKey(id, name)


if __name__ == '__main__':
    create_db(':memory:')
    pass
