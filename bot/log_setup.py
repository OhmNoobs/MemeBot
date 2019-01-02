import os
import sys
import logging
from logging import handlers
FIVE_MEGABYTE = 2**20 * 5


def setup():
    the_log = init_logger()
    return the_log


def init_logger() -> logging.Logger:
    setup_working_directory()
    the_log = logging.getLogger('')
    the_log.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    add_stream_handler(formatter, the_log)
    add_file_handler(formatter, the_log)
    logging.info('Started logging')
    return the_log


def setup_working_directory():
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    os.chdir(dir_name)


def add_file_handler(formatter, the_log) -> None:
    fh = handlers.RotatingFileHandler('meme_bot.log', maxBytes=FIVE_MEGABYTE, backupCount=7)
    fh.setFormatter(formatter)
    the_log.addHandler(fh)


def add_stream_handler(formatter, the_log) -> None:
    ch = logging.StreamHandler(sys.stderr)
    ch.setFormatter(formatter)
    the_log.addHandler(ch)
