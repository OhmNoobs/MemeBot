import logging
from typing import List, Optional
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update

from functions.Mozartizer import Mozartizer
from common import Sentence
from neocortex import memories
from neocortex.memories import valid_username

processed_inline_kudos = {}
log = logging.getLogger()
KUDOS_CALLBACK_ID_PREFIX = 'kudos-'


def create_reply_from(update: Update) -> List[InlineQueryResultArticle]:
    user_input = Sentence(update.inline_query.query)
    return _create_result_articles(user_input)


def _create_result_articles(query: Sentence) -> List[InlineQueryResultArticle]:
    results = [_generate_mozartized_article(query)]
    kudos_article = _generate_kudos_article(query)
    if kudos_article:
        results.append(kudos_article)
    return results


def _generate_mozartized_article(query: Sentence):
    mozartized = Mozartizer(query).mozartize()
    if not mozartized:
        mozartized = 'Mnmnmnnn'

    return InlineQueryResultArticle(
        id=uuid4(),
        title="Mozartize",
        description="Get a mumbled version of your input.",
        input_message_content=InputTextMessageContent(mozartized))


def _generate_kudos_article(query: Sentence) -> Optional[InlineQueryResultArticle]:
    mentioned_users = [word[1:] for word in query.word_list if word.startswith("@") and valid_username(word[1:])]
    if not mentioned_users:
        return None
    user_names = ' '.join(mentioned_users)
    callback_key = f'{KUDOS_CALLBACK_ID_PREFIX}{uuid4()}'
    processed_inline_kudos[str(callback_key)] = mentioned_users
    return InlineQueryResultArticle(
        id=callback_key,
        title="Give Kudos",
        description=user_names,
        input_message_content=InputTextMessageContent(f"Gave kudos to {user_names}"))


def process_callback(update: Update) -> None:
    sender = memories.remember_telegram_user(update.effective_user)
    if not _is_kudos_result_id(update.chosen_inline_result.result_id):
        return
    receivers = _link_to_inline_result(update.chosen_inline_result.result_id)

    for receiver in receivers:
        receiver = memories.remember_username(receiver)
        memories.give_kudos(sender, receiver)


def _is_kudos_result_id(result_id: str) -> bool:
    return result_id.startswith(KUDOS_CALLBACK_ID_PREFIX)


def _link_to_inline_result(callback_id: str) -> List[str]:
    try:
        receivers = processed_inline_kudos[callback_id]
    except KeyError:
        log.info("Update couldn't be linked to sent inline response.")
        return []
    return receivers
