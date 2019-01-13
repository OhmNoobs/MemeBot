import os
import random
from functools import wraps
from typing import List, Union

import telegram

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION = "this is the box where i keep my old memories: https://i.imgur.com/WqLMDE3.jpg feat. kudos"
START_HELP = """
*mozartize* - Get a mozartized version of your input
*aehxtend* - Get a ähxtended version of your input
*food* - Get some food!
*exmatrikulieren* - Generiert eine Exmatrikulation für arg1 arg2, arg3 ... argN ist der Grund.
*notify_me* - Toggle notifications
*version* - Get the version

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


def fortune_is_willing(probability=0.5) -> bool:
    if 0 < probability > 1:
        raise ValueError("Choose a value between 0 and 1")
    probability *= 100
    return random.randrange(0, 100) < probability


def text_wrap(text, font, max_width) -> List[str]:
    lines = [""]
    if font.getsize(text)[0] <= max_width:
        lines[-1] = text
    else:
        words = text.split(' ')
        for word in words:
            if font.getsize(word)[0] > max_width:
                # if the word is to large for a single line, truncate until it fits.
                while font.getsize(word + "...")[0] > max_width:
                    word = word[:-1]
                word = word + "..."
            if font.getsize(lines[-1] + word)[0] <= max_width:
                # append word to last line
                lines[-1] = lines[-1] + word + " "
            else:
                # when the line gets longer than the max width append it to new line.
                lines.append(word + " ")
    return lines


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
        bot, update = args
        bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(bot, update, **kwargs)

    return command_func
