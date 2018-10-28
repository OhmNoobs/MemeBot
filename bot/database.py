from pony.orm import *

db = Database()


class TelegramUser(db.Entity):
    name = PrimaryKey(str)


db.bind(provider='sqlite', filename='database', create_db=True)
db.generate_mapping(create_tables=True)
