from telegram.ext import CommandHandler, InlineQueryHandler, Updater

import helper
import functions
import log_setup


def main():
    updater = Updater(helper.get_bot_token())
    log.debug('Updater created')
    attach_handlers(updater.dispatcher)
    log.debug('Handlers attached')
    updater.start_polling()
    log.debug('Going into idle...')
    updater.idle()


def attach_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', functions.start))
    dispatcher.add_handler(CommandHandler('hello', functions.hello))
    dispatcher.add_handler(CommandHandler('version', functions.version))
    dispatcher.add_handler(CommandHandler('mozartize', functions.mozartize, pass_args=True))
    dispatcher.add_handler(CommandHandler('aehxtend', functions.aehxtend, pass_args=True))
    dispatcher.add_handler(CommandHandler('food', functions.food))
    dispatcher.add_handler(CommandHandler('joke', functions.joke, pass_args=True))
    dispatcher.add_handler(CommandHandler('exmatrikulieren', functions.exmatriculate, pass_args=True))
    dispatcher.add_handler(CommandHandler('notify_me', functions.notifier, pass_job_queue=True))
    dispatcher.add_handler(InlineQueryHandler(functions.inline_query))
    dispatcher.add_error_handler(error_logger)


def error_logger(_, update, error) -> None:
    log.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    log = log_setup.init_logger()
    main()
