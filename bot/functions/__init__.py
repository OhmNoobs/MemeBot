import telegram
from telegram import Update
from telegram.ext import CallbackContext

from functions import food_scraper, inline_bot, Exmatriculator, Notifier
from functions.Aehxtender import Aehxtender
from functions.Mozartizer import Mozartizer
from functions.joke import make_joke_about
from functions.kudos import KudosMessageParser
from functions.ToiletPaper import ToiletPaper
from functions.Matomat import Matomat
from common import Sentence, send_typing_action, restricted


def hello(update: Update, _) -> None:
    update.message.reply_text(helpers.greet_user(update.message.from_user.first_name))


def start(update: Update, _):
    update.message.reply_text(helpers.help_user(update.message.from_user.first_name),
                              parse_mode=telegram.ParseMode.MARKDOWN)


def version(update: Update, _) -> None:
    update.message.reply_text(helpers.version())


def mozartize(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Mozartizer(Sentence(context.args)).mozartize())


def aehxtend(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Aehxtender(Sentence(context.args)).get_aehxtended())


def inline_query(update: Update, _) -> None:
    update.inline_query.answer(inline_bot.create_reply_from(update))


def inline_query_feedback(update: Update, _) -> None:
    inline_bot.process_callback(update)


@send_typing_action
def food(update: Update, _) -> None:
    update.message.reply_text(food_scraper.order(), parse_mode=telegram.ParseMode.MARKDOWN)


@send_typing_action
def joke(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(make_joke_about(context.args))


@send_typing_action
def exmatriculate(update: Update, context: CallbackContext) -> None:
    exmatriculation = Exmatriculator.generate_exmatriculation(context.args)
    if exmatriculation:
        context.bot.send_photo(update.message.chat_id, photo=exmatriculation.form, caption=exmatriculation.description)
    else:
        update.message.reply_text("Usage: /exmatrikulieren Vorname Nachname Grund bla bla bla")


def notifier(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Notifier.manage_subscription(update.message.from_user, context.job_queue))


@send_typing_action
def kudos(update: Update, _) -> None:
    update.message.reply_text(KudosMessageParser(update).handle_kudos_command())


@send_typing_action
def toilet_paper(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(ToiletPaper(context.args).wrap())


def matomat(_, update) -> None:
    update.message.reply_text('Kaufen:', reply_markup=Matomat.open_keyboard())


@send_typing_action
def buy(_, update, args) -> None:
    update.message.reply_text(Matomat.buy(update.effective_user, args))


@restricted
def add_product(_, update, args) -> None:
    update.message.reply_text(Matomat.add_product(args))


@send_typing_action
def deposit(_, update, args):
    update.message.reply_text(Matomat.deposit(update.effective_user, args))
