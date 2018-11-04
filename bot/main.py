import logging
import os
import sys
from uuid import uuid4

import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent

from functions import food_scraper
from logging import handlers
from functions.Mozartizer import Mozartizer
from functions.Aehxtender import Aehxtender
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from functions.Exmatriculator import exmatriculate
from functions.joke import make_joke_about
from helper import Sentence


VERSION = "ES GIBT DÖNER!"


def hello(_, update) -> None:
    update.message.reply_text(f'Hello {update.message.from_user.first_name}')


def mozartize(_, update, args) -> None:
    update.message.reply_text(Mozartizer(Sentence(args)).mozartize())


def aehxtend(_, update, args) -> None:
    update.message.reply_text(Aehxtender(Sentence(args)).get_aehxtended())


def food(_, update) -> None:
    update.message.reply_text(food_scraper.order(), parse_mode=telegram.ParseMode.MARKDOWN)


def joke(_, update, args) -> None:
    update.message.reply_text(make_joke_about(args))


def version(_, update) -> None:
    update.message.reply_text(VERSION)


def error_logger(_, update, error) -> None:
    log.warning('Update "%s" caused error "%s"', update, error)


def inline_query(_, update):
    """Handle the inline query."""
    query = update.inline_query.query
    aehxtended = Aehxtender(Sentence(query)).get_aehxtended()
    if not aehxtended:
        aehxtended = 'äh'
    mozartized = Mozartizer(Sentence(query)).mozartize()
    if not mozartized:
        mozartized = 'Mnmnmnnn'
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Ähxtend",
            description="Ähxtends your sentence!",
            input_message_content=InputTextMessageContent(aehxtended)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Mozartize",
            description="Get a mumbled version of your input.",
            input_message_content=InputTextMessageContent(mozartized))
    ]
    update.inline_query.answer(results)


def main():
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('version', version))
    updater.dispatcher.add_handler(CommandHandler('mozartize', mozartize, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('aehxtend', aehxtend, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('food', food))
    updater.dispatcher.add_handler(CommandHandler('joke', joke, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('exmatrikulieren', exmatriculate, pass_args=True))
    updater.dispatcher.add_handler(InlineQueryHandler(inline_query))
    updater.dispatcher.add_error_handler(error_logger)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    os.chdir(dir_name)
    log = logging.getLogger('')
    log.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler(sys.stderr)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    fh = handlers.RotatingFileHandler('meme_bot.log', maxBytes=(1048576 * 5), backupCount=7)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    logging.info('Started logging')

    try:
        bot_token = os.environ['BOT_TOKEN']
    except KeyError as e:
        raise Exception("No bot token specified. Please provide one via environment variable 'BOT_TOKEN'.")

    updater = Updater(bot_token)

    main()
