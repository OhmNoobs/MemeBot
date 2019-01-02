import os
import logging
import sys
from logging import handlers
FIVE_MEGABYTE = 2**20 * 5
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def init_logger() -> logging.Logger:
    setup_working_directory()
    the_log = logging.getLogger('meme-bot')
    the_log.setLevel(logging.INFO)
    the_log.addHandler(add_stream_handler())
    the_log.addHandler(add_file_handler())
    the_log.info('Started logging')
    return the_log


def setup_working_directory():
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    os.chdir(dir_name)


def add_file_handler() -> logging.FileHandler:
    log_to_file = handlers.RotatingFileHandler('meme_bot.log', maxBytes=FIVE_MEGABYTE, backupCount=7)
    log_to_file.setFormatter(FORMATTER)
    return log_to_file


def add_stream_handler() -> logging.StreamHandler:
    log_to_console = logging.StreamHandler(sys.stdout)
    log_to_console.setFormatter(FORMATTER)
    return log_to_console
