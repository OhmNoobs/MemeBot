import logging
import os
import sys
import telegram

from functions import food_scraper
from logging import handlers
from functions.Mozartizer import Mozartizer
import functions.aehxtender as aehxtender
from telegram.ext import Updater, CommandHandler
from functions.th_remover import remove_from_th
from functions.joke import make_joke_about


VERSION = "refactored"


def hello(_, update) -> None:
    update.message.reply_text(f'Hello {update.message.from_user.first_name}')


def mozartize(_, update, args) -> None:
    update.message.reply_text(Mozartizer(args).mozartize())


def aehxtend(_, update, args) -> None:
    update.message.reply_text(aehxtender.aehxtend(args))


def food(_, update) -> None:
    update.message.reply_text(food_scraper.serve(), parse_mode=telegram.ParseMode.MARKDOWN)


def joke(_, update, args) -> None:
    update.message.reply_text(make_joke_about(args))


def kudos(bot, update) -> None:
    pass


def version(_, update) -> None:
    update.message.reply_text(VERSION)


def main():
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('version', version))
    updater.dispatcher.add_handler(CommandHandler('mozartize', mozartize, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('aehxtend', aehxtend, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('food', food))
    updater.dispatcher.add_handler(CommandHandler('joke', joke, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('kudos', kudos))
    updater.dispatcher.add_handler(CommandHandler('exmatrikulieren', remove_from_th, pass_args=True))
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
        logging.fatal("No bot token specified. Please provide one via environment variable 'BOT_TOKEN'.")
        raise e

    updater = Updater(bot_token)

    main()
