import logging
from typing import List, NamedTuple, Optional

import telegram

from exceptions import TooPoorException
from neocortex import memories

log = logging.getLogger()


class ProductDescription(NamedTuple):
    name: str
    price: float
    description: str


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
    except TooPoorException as e:
        return "Your are too poor."
    return "Success."


def add_product(args: List[str]):
    product_description = extract_product_description(args)
    product = memories.memorize_product(product_description)
    return f"{product.name} ({product.price}€) added."
