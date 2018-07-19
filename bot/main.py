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

VERSION = "so many reasons..."
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
    pass


def remove_from_th(bot, update, args) -> None:
    surname = ""
    last_name = ""
    reason = "Noob."
    if len(args) > 0:
        if len(args) > 0:
            surname = args[0].capitalize()
        if len(args) > 1:
            last_name = args[1].capitalize()
        if len(args) > 2:
            reason = " ".join(args[2:])

    else:
        update.message.reply_text("Usage: /exmatrikulieren Vorname Nachname Grund bla bla bla")
        return

    image = Image.open("removal_form.png")
    drawing = ImageDraw.Draw(image)
    sans_serif = ImageFont.truetype("Roboto-Regular.ttf", 16)
    hand_writing = ImageFont.truetype("DawningofaNewDay.ttf", 22)
    hand_writing_small = ImageFont.truetype("DawningofaNewDay.ttf", 18)
    drawing.text((120, 90), last_name, (0, 0, 0), font=sans_serif)
    drawing.text((420, 90), surname, (0, 0, 0), font=sans_serif)
    drawing.text((420, 210), date.today().strftime("%d.%m.%Y"), (0, 0, 0), font=sans_serif)
    drawing.text((170, 360), date.today().strftime("%m/%Y"), (0, 0, 0), font=sans_serif)
    drawing.text((420, 759), f"{surname} {last_name}", (0, 81, 158), font=hand_writing)
    reason_multi_line = text_wrap(reason, hand_writing_small, 568)
    drawing.text((40, 635), "\n".join(reason_multi_line[:2]), (0, 81, 158), font=hand_writing_small)
    drawing.text((40, 773), "Nürnberg, " + date.today().strftime("%d. %B %Y"), (0, 81, 158), font=hand_writing_small)
    bio = BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'png')
    bio.seek(0)
    bot.send_photo(update.message.chat_id, photo=bio)
    pass


def text_wrap(text, font, max_width):
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
        logging.fatal("No bot token specified. Please provide it via environment variable 'BOT_TOKEN'.")
        raise e

    updater = Updater(bot_token)

    main(updater)
