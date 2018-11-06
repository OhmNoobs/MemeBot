import telegram

from functions import food_scraper, inline_bot, Exmatriculator
from functions.Aehxtender import Aehxtender
from functions.Mozartizer import Mozartizer
from functions.joke import make_joke_about
from helper import Sentence, VERSION


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


def exmatriculate(bot, update, args) -> None:
    exmatriculation = Exmatriculator.generate_exmatriculation(args)
    if exmatriculation:
        bot.send_photo(update.message.chat_id, photo=exmatriculation)
    else:
        update.message.reply_text("Usage: /exmatrikulieren Vorname Nachname Grund bla bla bla")


def version(_, update) -> None:
    update.message.reply_text(VERSION)


def inline_query(_, update) -> None:
    update.inline_query.answer(inline_bot.process(update))
