import telegram
from telegram import Update
from telegram.ext import CallbackContext

from functions import food_scraper, inline_bot, Exmatriculator, Notifier, helpers
from functions.Mozartizer import Mozartizer
from functions.joke import make_joke_about
from functions.kudos import KudosMessageParser
from functions.ToiletPaper import ToiletPaper
import functions.Matomat as Matomat
from common import Sentence, send_typing_action, restricted


def hello(update: Update, _) -> None:
    update.message.reply_text(helpers.greet_user(update.message.from_user.first_name))


def start(update: Update, _):
    update.message.reply_text(helpers.help_user(update.message.from_user.first_name),
                              parse_mode=telegram.ParseMode.MARKDOWN_V2)


def version(update: Update, _) -> None:
    update.message.reply_text(helpers.version())


def mozartize(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Mozartizer(Sentence(context.args)).mozartize())


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


def matomat(update: Update, _) -> None:
    update.message.reply_text('Kaufen:', reply_markup=Matomat.open_keyboard())


@send_typing_action
def buy(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Matomat.buy(update.effective_user, context.args))


@restricted
def add_product(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Matomat.add_product(context.args), parse_mode=telegram.ParseMode.MARKDOWN_V2)


@send_typing_action
def deposit(update: Update, context: CallbackContext):
    update.message.reply_text(Matomat.deposit(update.effective_user, context.args))
