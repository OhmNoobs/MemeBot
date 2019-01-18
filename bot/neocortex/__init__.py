import datetime
import logging
import os
from pathlib import Path
from typing import Union

from pony.orm import Database, PrimaryKey, Optional, Set, Required

DB_FILE = Path(os.path.abspath(__file__)).parent / 'neocortex.sqlite'
db = Database()
log = logging.getLogger()


def bind_db(filename: Path = DB_FILE):
    if DB_FILE.is_file():
        db.bind(provider='sqlite', filename=filename)
        db.generate_mapping()
    else:
        log.info("Database file doesn't exist. Creating...")
        create_db(filename.name)


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


class Kudos(db.Entity):
    id = PrimaryKey(int, auto=True)
    giver = Required(User, reverse='kudos_given')
    taker = Required(User, reverse='kudos_received')
    timestamp = Required(datetime.datetime)


if __name__ == '__main__':
    create_db(':memory:')
