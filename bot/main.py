import logging
import os

from telegram.ext import Updater, CommandHandler


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def main():
    try:
        bot_token = os.environ['BOT_TOKEN']
    except KeyError:
        logging.fatal("No bot token specified. Please provide it via environment variable 'BOT_TOKEN'.")
        return

    updater = Updater(bot_token)

    updater.dispatcher.add_handler(CommandHandler('hello', hello))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(filename='meme_bot.log', level=logging.INFO)
    logging.info('Started logging')
    main()
