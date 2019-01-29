import logging
from typing import List

import telegram

log = logging.getLogger()


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


def interpret() -> telegram.ReplyKeyboardMarkup:
    buttons = [telegram.KeyboardButton('Mate (0,70€)'), telegram.KeyboardButton('Cola (0,70€)'),
               telegram.KeyboardButton('Wasser (0,50€)')]
    menu = build_menu(buttons, 2)
    return telegram.ReplyKeyboardMarkup(menu)
