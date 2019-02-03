import telegram

from functions import food_scraper, inline_bot, Exmatriculator, Notifier, Matomat
from functions.Aehxtender import Aehxtender
from functions.Mozartizer import Mozartizer
from functions.joke import make_joke_about
from functions.kudos import KudosMessageParser
from helper import Sentence, VERSION, START_HELP, send_typing_action, restricted


def hello(_, update) -> None:
    update.message.reply_text(f'Hello {update.message.from_user.first_name}')


def start(_, update):
    update.message.reply_text(f'Hi {update.message.from_user.first_name} ich kann folgendes: {START_HELP}.',
                              parse_mode=telegram.ParseMode.MARKDOWN)


def version(_, update) -> None:
    update.message.reply_text(VERSION)


def mozartize(_, update, args) -> None:
    update.message.reply_text(Mozartizer(Sentence(args)).mozartize())


def aehxtend(_, update, args) -> None:
    update.message.reply_text(Aehxtender(Sentence(args)).get_aehxtended())


def inline_query(_, update) -> None:
    update.inline_query.answer(inline_bot.create_reply_from(update))


def inline_query_feedback(_, update) -> None:
    inline_bot.process_callback(update)


@send_typing_action
def food(_, update) -> None:
    update.message.reply_text(food_scraper.order(), parse_mode=telegram.ParseMode.MARKDOWN)


@send_typing_action
def joke(_, update, args) -> None:
    update.message.reply_text(make_joke_about(args))


@send_typing_action
def exmatriculate(bot, update, args) -> None:
    exmatriculation = Exmatriculator.generate_exmatriculation(args)
    if exmatriculation:
        bot.send_photo(update.message.chat_id, photo=exmatriculation.form, caption=exmatriculation.description)
    else:
        update.message.reply_text("Usage: /exmatrikulieren Vorname Nachname Grund bla bla bla")


def notifier(_, update, job_queue) -> None:
    update.message.reply_text(Notifier.manage_subscription(update.message.from_user, job_queue))


@send_typing_action
def kudos(_, update) -> None:
    update.message.reply_text(KudosMessageParser(update).handle_kudos_command())


def matomat(_, update) -> None:
    update.message.reply_text('Kaufen:', reply_markup=Matomat.open_keyboard())


@send_typing_action
def buy(_, update, args) -> None:
    update.message.reply_text(Matomat.buy(update.effective_user, args))


@restricted
def add_product(_, update, args) -> None:
    update.message.reply_text(Matomat.add_product(args))
