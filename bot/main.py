import logging
import os
import random

os.urandom(2)

from telegram.ext import Updater, CommandHandler

VERSION = "0.1"

def hello(bot, update):
    update.message.reply_text(f'Hello {update.message.from_user.first_name}')


def mozartize(bot, update, args):
    out = ""
    i = 0
    for word in args:
        if i != 0:
            out += ' '
        if fortune_is_willing():
            mozartized_word = ''
            for _ in word:
                if fortune_is_willing():
                    mozartized_word += 'n' if fortune_is_willing() else 'N'
                else:
                    mozartized_word += 'M' if fortune_is_willing() else 'm'
            out += mozartized_word
        else:
            out += word
        i += 1
    update.message.reply_text(out)


def fortune_is_willing():
    return bool(random.getrandbits(1))

def aehxtend(bot, update, args):
    update.message.reply_text(f"Coming soon™️")


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
    updater.dispatcher.add_handler(CommandHandler('mozartize', mozartize, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('ähxtend', aehxtend, pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(filename='meme_bot.log', level=logging.INFO)
    logging.info('Started logging')
    main()
