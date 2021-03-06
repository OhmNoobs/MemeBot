from telegram import Update
from telegram.ext import CommandHandler, InlineQueryHandler, Updater, ChosenInlineResultHandler, CallbackContext

import common
import functions
import log_setup
import neocortex


def main():
    updater = Updater(common.get_bot_token(), use_context=True)
    log.info('Updater created')
    attach_handlers(updater.dispatcher)
    log.info('Handlers attached')
    neocortex.bind_db()
    log.info('Made memories accessible')
    functions.Notifier.remember_subscribers(bot=updater.bot, queue=updater.job_queue)
    log.info('Remembered previous subscribers.')
    updater.start_polling()
    log.info('Going into idle...')
    updater.idle()


def attach_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', functions.start))
    dispatcher.add_handler(CommandHandler('hello', functions.hello))
    dispatcher.add_handler(CommandHandler('version', functions.version))
    dispatcher.add_handler(CommandHandler('mozartize', functions.mozartize))
    dispatcher.add_handler(CommandHandler('food', functions.food))
    dispatcher.add_handler(CommandHandler('joke', functions.joke))
    dispatcher.add_handler(CommandHandler('exmatrikulieren', functions.exmatriculate))
    dispatcher.add_handler(CommandHandler('notify_me', functions.notifier))
    dispatcher.add_handler(CommandHandler('kudos', functions.kudos))
    dispatcher.add_handler(CommandHandler('matomat', functions.matomat))
    dispatcher.add_handler(CommandHandler('buy', functions.buy))
    dispatcher.add_handler(CommandHandler('add_product', functions.add_product))
    dispatcher.add_handler(CommandHandler('deposit', functions.deposit))
    dispatcher.add_handler(CommandHandler('paper', functions.toilet_paper))
    dispatcher.add_handler(InlineQueryHandler(functions.inline_query))
    dispatcher.add_handler(ChosenInlineResultHandler(functions.inline_query_feedback))
    dispatcher.add_error_handler(error_logger)


def error_logger(update: Update, context: CallbackContext) -> None:
    log.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    log = log_setup.init_logger()
    main()
