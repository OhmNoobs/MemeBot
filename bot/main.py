import logging
import os

import sys
from logging import handlers
from bot.helper import fortune_is_willing
from bot import Mozartizer

from telegram.ext import Updater, CommandHandler

VERSION = "Ähxtended!"


def hello(bot, update):
    update.message.reply_text(f'Hello {update.message.from_user.first_name}')


def mozartize_sentence(bot, update, args):
    update.message.reply_text(Mozartizer(args).mozartize())


def aehxtend(bot, update, args):
    sentence = ' '.join(args)
    i = 0
    while i < len(sentence):
        if fortune_is_willing() and fortune_is_willing() and fortune_is_willing():
            pre_padding = '' if i == 0 or sentence[i-1] == ' ' or sentence[i-1] == '-' else '-'
            post_padding = '' if i == len(sentence) or sentence[i] == ' ' or sentence[i] == '-' else '-'
            aehxtension = f"{pre_padding}äh{post_padding}"
            sentence = sentence[:i] + aehxtension + sentence[i:]
            i = i + 4  # length of one ähxtension
        else:
            i += 1
    update.message.reply_text(sentence)


def version(bot, update):
    update.message.reply_text(VERSION)


def main():
    try:
        bot_token = os.environ['BOT_TOKEN']
    except KeyError:
        logging.fatal("No bot token specified. Please provide it via environment variable 'BOT_TOKEN'.")
        return
    
    updater = Updater(bot_token)
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('version', version))
    updater.dispatcher.add_handler(CommandHandler('mozartize', mozartize_sentence, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('ähxtend', aehxtend, pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    fh = handlers.RotatingFileHandler('meme_bot.log', maxBytes=(1048576 * 5), backupCount=7)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    logging.info('Started logging')
    main()
