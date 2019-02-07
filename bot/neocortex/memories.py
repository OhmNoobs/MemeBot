import re
import typing
from datetime import datetime, timedelta
from typing import Iterator

import telegram
from pony.orm import db_session, desc, select

from exceptions import TooPoorException, TooRichException, FloodingError
from functions.Matomat import ProductDescription, MAXIMUM_DEPOSIT
from neocortex import log, User, Kudos, Product, Transaction

UserNameValidator = re.compile(r"([a-zA-Z0-9_]){5,32}")
DEPOSIT = 'deposit'
RECENT_TIMESPAN = timedelta(hours=1, minutes=30)
TRANSACTION_FLOODING_THRESHOLD = 10
DEPOSIT_FLOODING_THRESHOLD = 3
blocked_users = {}


class TopKudosReceiver(typing.NamedTuple):
    name: str
    kudos_received: int


@db_session
def remember_blocked_users() -> typing.List[User]:
    return list(User.select(lambda user: user.banned_until))


@db_session
def block_user(user: User, block_expiry: datetime):
    User[user.internal_id].banned_until = block_expiry


@db_session
def unblock_user(user):
    User[user.internal_id].banned_until = None


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
def _create_or_update(user: telegram.User) -> User:
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


def _prepare_for_update(user) -> dict:
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
def get_kudos_of_user(user: User) -> int:
    return len(User[user.internal_id].kudos_received)


@db_session
def get_all_products() -> typing.List[Product]:
    return Product.get()


@db_session
def remember_shop_owner() -> User:
    shop_owner = User.get(username="FSIN")
    if not shop_owner:
        shop_owner = User(first_name="FS", last_name="IN", username="FSIN", wants_notifications=False)
    return shop_owner


def _to_telegram_user(user: User) -> telegram.User:
    subscriber = user.to_dict()
    subscriber["id"] = subscriber.pop("telegram_id")
    return telegram.User(**subscriber)


def valid_username(username) -> bool:
    """
    According to https://core.telegram.org/method/account.checkUsername:
    Accepted characters: A-z (case-insensitive), 0-9 and underscores. Length: 5-32 characters.
    """
    return len(UserNameValidator.findall(username)) == 1


@db_session
def memorize_transaction(from_user: User, to_user: User, amount: float) -> float:
    sender = User[from_user.internal_id]
    receiver = User[to_user.internal_id]
    _transaction_flooding_protection(sender)
    if sender == receiver:
        return _memorize_deposit_transaction(sender, receiver, amount)
    else:
        return _memorize_transfer_transaction(sender, receiver, amount)


# noinspection PyTypeChecker
def _transaction_flooding_protection(depositor: User) -> None:
    recent_transactions_by_depositor = select(
        t for t in Transaction if t.timestamp >= datetime.now() - RECENT_TIMESPAN and t.sender == depositor
    )[:]
    if len(recent_transactions_by_depositor) > TRANSACTION_FLOODING_THRESHOLD:
        log.warning(f"Transaction flooding by @{User.username} detected")
        raise FloodingError('Too many transactions.', depositor)
    recent_deposits = [
        transaction for transaction in recent_transactions_by_depositor if transaction.description == DEPOSIT
    ]
    if len(recent_deposits) > DEPOSIT_FLOODING_THRESHOLD:
        log.warning(f"Deposit flooding by @{User.username} detected")
        raise FloodingError('Too many deposits. Please wait before making attempting any more deposits.', depositor)
    pass  # yay!


@db_session
def _memorize_deposit_transaction(sender: User, receiver: User, amount: float) -> float:
    if not receiver.balance:
        receiver.balance = 0
    if amount > MAXIMUM_DEPOSIT or (receiver.balance and receiver.balance + amount > MAXIMUM_DEPOSIT):
        raise TooRichException()
    Transaction(sender=sender, receiver=receiver, amount=amount, timestamp=datetime.now(), description=DEPOSIT)
    receiver.balance = receiver.balance + amount
    return receiver.balance


@db_session
def _memorize_transfer_transaction(sender: User, receiver: User, amount: float) -> float:
    if sender.balance >= amount:
        Transaction(sender=sender, receiver=receiver, amount=amount, timestamp=datetime.now())
        sender.balance = sender.balance - amount
        receiver.balance = receiver.balance + amount
    else:
        raise TooPoorException()
    return sender.balance


@db_session
def remember_product(description: ProductDescription) -> Product:
    return Product.get(lambda product:
                       product.name == description.name
                       and product.price == description.price
                       and product.description == description.description)


@db_session
def remember_all_products() -> typing.List[Product]:
    return Product.select()[:]


@db_session
def memorize_product(product: ProductDescription, for_sale: bool = True, image_path: str = None) -> Product:
    return Product(name=product.name,
                   price=product.price,
                   description=product.description,
                   image_path=image_path,
                   for_sale=for_sale)


