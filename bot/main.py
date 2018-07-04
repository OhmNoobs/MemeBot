import logging
import os
import sys

import requests
import food_scraper
import telegram
import re

from datetime import date
from logging import handlers
from Mozartizer import Mozartizer
from helper import fortune_is_willing
from telegram.ext import Updater, CommandHandler
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO


VERSION = "FOOOOOD!"
CHUCK_API = "https://api.chucknorris.io/jokes/random"
CHUCK = re.compile("chuck", re.IGNORECASE)
NORRIS = re.compile("norris", re.IGNORECASE)


def hello(bot, update) -> None:
    update.message.reply_text(f'Hello {update.message.from_user.first_name}')


def mozartize_sentence(bot, update, args) -> None:
    update.message.reply_text(Mozartizer(args).mozartize())


def aehxtend(bot, update, args) -> None:
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


def food(bot, update) -> None:
    update.message.reply_text(food_scraper.serve(), parse_mode=telegram.ParseMode.MARKDOWN)


def chuck(bot, update, args) -> None:
    response = requests.get(CHUCK_API).json()
    joke = response["value"]  # type: str
    if args:
        if len(args) > 0:
            joke = CHUCK.sub(args[0].capitalize(), joke)
        if len(args) > 1:
            joke = NORRIS.sub(args[1].capitalize(), joke)
    if joke:
        update.message.reply_text(joke)


def kudos(bot, update) -> None:
    # 
    pass


def remove_from_th(bot, update, args) -> None:
    surname = ""
    last_name = ""
    reason = "Noob."
    if len(args) > 0:
        if len(args) > 0:
            surname = args[0]
        if len(args) > 1:
            last_name = args[1]
        if len(args) > 2:
            reason = " ".join(args[2:])

    image = Image.open("/usr/src/app/bot/removal_form.png")
    drawing = ImageDraw.Draw(image)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    sans_serif = ImageFont.truetype("Roboto-Regular.ttf", 16)
    hand_writing = ImageFont.truetype("DawningofaNewDay.ttf", 22)
    hand_writing_small = ImageFont.truetype("DawningofaNewDay.ttf", 18)
    # draw.text((x, y),"Sample Text",(r,g,b))
    drawing.text((120, 90), last_name, (0, 0, 0), font=sans_serif)
    drawing.text((420, 90), surname, (0, 0, 0), font=sans_serif)
    drawing.text((420, 210), date.today().strftime("%d.%m.%Y"), (0, 0, 0), font=sans_serif)
    drawing.text((170, 360), date.today().strftime("%m/%Y"), (0, 0, 0), font=sans_serif)
    drawing.text((420, 759), f"{surname} {last_name}", (0, 81, 158), font=hand_writing)
    drawing.text((40, 645), reason, (0, 81, 158), font=hand_writing_small)
    drawing.text((40, 773), "Nürnberg, " + date.today().strftime("%d. %B %Y"), (0, 81, 158), font=hand_writing_small)
    bio = BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'png')
    bio.seek(0)
    bot.send_photo(update.message.chat_id, photo=bio)
    pass


def version(bot, update) -> None:
    update.message.reply_text(VERSION)


def main(updater):
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('version', version))
    updater.dispatcher.add_handler(CommandHandler('mozartize', mozartize_sentence, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('aehxtend', aehxtend, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('food', food))
    updater.dispatcher.add_handler(CommandHandler('joke', chuck, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('kudos', kudos))
    updater.dispatcher.add_handler(CommandHandler('exmatrikulieren', remove_from_th, pass_args=True))

    job_queue = updater.job_queue

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
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
        logging.fatal("No bot token specified. Please provide it via environment variable 'BOT_TOKEN'.")
        raise e

    updater = Updater(bot_token)

    main(updater)
