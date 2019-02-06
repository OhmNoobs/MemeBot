import datetime
import logging
from functools import wraps
from typing import List, NamedTuple, Optional

import telegram

from exceptions import TransactionError, FloodingError
from neocortex import memories

log = logging.getLogger()
INVALID_DEPOSIT_ARGS = "Invalid arguments. Use this like /deposit 20,3"
MINIMUM_DEPOSIT = 0.01
MAXIMUM_DEPOSIT = 50
BASE_BLOCK_DURATION = datetime.timedelta(hours=1, minutes=30)


class ProductDescription(NamedTuple):
    name: str
    price: float
    description: str


def flooding_protected_transaction_request(func):

    @wraps(func)
    def wrapped(user: telegram.User, arguments: List[str], *args, **kwargs):
        blocked_users = memories.remember_blocked_users()
        if user.id in blocked_users and blocked_users[user.id] < datetime.datetime.now():
            return
        try:
            return func(user, arguments, *args, **kwargs)
        except FloodingError as flooding_error:
            blocked_until = datetime.datetime.now() + BASE_BLOCK_DURATION
            memories.block_user(flooding_error.offender)
            return f"{flooding_error} You are blocked from making any transactions until {blocked_until}"

    return wrapped


def build_menu(buttons: List[telegram.KeyboardButton],
               n_cols: int,
               header_buttons: List[telegram.KeyboardButton] = None,
               footer_buttons: List[telegram.KeyboardButton] = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def open_keyboard() -> telegram.ReplyKeyboardMarkup:
    buttons = [telegram.KeyboardButton('/buy Mate (0,70€)'), telegram.KeyboardButton('/buy Cola (0,70€)'),
               telegram.KeyboardButton('/buy Wasser (0,50€)')]
    menu = build_menu(buttons, 2)
    return telegram.ReplyKeyboardMarkup(menu)


def extract_product_description(args: List[str]) -> Optional[ProductDescription]:
    if len(args) < 2:
        return None
    if len(args) < 3:
        description = None
    else:
        description = ' '.join(args[2:])
    price = args[1][1:-2]
    price = price.replace(',', '.')
    return ProductDescription(name=args[0], price=float(price), description=description)


@flooding_protected_transaction_request
def buy(user: telegram.User, args: List[str]) -> str:
    customer = memories.remember_telegram_user(user)
    product_description = extract_product_description(args)
    if not product_description:
        return "Use the Keyboard provided by /buy"
    shop_owner = memories.remember_shop_owner()
    item = memories.remember_product(product_description)
    if not item:
        return "Product currently unavailable."
    try:
        memories.memorize_transaction(from_user=customer, to_user=shop_owner, amount=item.price)
    except TransactionError as transaction_error:
        return str(transaction_error)
    return "Success."


def add_product(args: List[str]):
    product_description = extract_product_description(args)
    product = memories.memorize_product(product_description)
    return f"{product.name} ({product.price}€) added."


@flooding_protected_transaction_request
def deposit(depositor: telegram.User, args: List[str]) -> str:
    if not args:
        return INVALID_DEPOSIT_ARGS
    amount = prepare_for_cast_to_float(args)
    try:
        amount = float(amount)
    except ValueError:
        return INVALID_DEPOSIT_ARGS
    if amount > MAXIMUM_DEPOSIT:
        return f"Deposits above {MAXIMUM_DEPOSIT}€ are not allowed."
    if amount < MINIMUM_DEPOSIT:
        return f"Deposits below {MINIMUM_DEPOSIT}€ are not allowed."
    internal_user = memories.remember_telegram_user(depositor)
    memories.memorize_transaction(internal_user, internal_user, amount)


def prepare_for_cast_to_float(args):
    amount = args[0]
    return amount.replace(',', '.').replace('€', '').replace('-', '')



