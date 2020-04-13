import os
import random
from functools import wraps
from typing import Union, List
import logging
import telegram

log = logging.getLogger()


def create_admin_list_from_env():
    admins_original = os.environ.get('ADMINS', None)
    admin_ids = None
    if admins_original:
        admin_ids_as_strings = admins_original.split(',')
        admin_ids = [int(admin) for admin in admin_ids_as_strings]
    if not admin_ids:
        log.warning("No admins defined.")
    else:
        log.info("Following IDs are admins: " + admins_original)
    return admin_ids


LIST_OF_ADMINS = create_admin_list_from_env()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION = "Transitioned to v12: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0"
START_HELP = """
*mozartize* - Get a mozartized version of your input
*aehxtend* - Get a ähxtended version of your input
*food* - Get some food!
*exmatrikulieren* - Generiert eine Exmatrikulation für arg1 arg2, arg3 ... argN ist der Grund.
*notify_me* - Toggle notifications
*version* - Get the version
*kudos* - Transfer some sweet sweet Internet points to another person by mentioning her.
*deposit* - Remember that you deposited some money!
*matomat* - Buy drinks and more.

mozartize und aehxtend gibts auch als *inline query*! Tippe: @ohm-noobs-meme-bot dein input.
"""


class Sentence:

    def __init__(self, list_of_words: Union[str, list]):
        if type(list_of_words) == str:
            self.word_list = list_of_words.split(' ')
        else:
            self.word_list = list_of_words

    def __repr__(self) -> str:
        return ' '.join(self.word_list)

    def as_list(self) -> List[str]:
        return self.word_list


def chance_to_return_true(probability=0.5) -> bool:
    if 0 < probability > 1:
        raise ValueError("Choose a value between 0 and 1")
    probability *= 100
    return random.randrange(0, 100) < probability


def get_bot_token() -> str:
    try:
        bot_token = os.environ['BOT_TOKEN']
    except KeyError as e:
        raise Exception("No bot token specified. Please provide one via environment variable 'BOT_TOKEN'.")
    return bot_token


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        update, context = args
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(update, context, **kwargs)

    return command_func


def restricted(func):
    @wraps(func)
    def wrapped(update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            log.info(f"Unauthorized access denied for {user_id}. Message: {update.message}")
            return
        return func(update, *args, **kwargs)

    return wrapped
