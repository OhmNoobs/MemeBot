import logging
from typing import List, Optional
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update

from functions.Aehxtender import Aehxtender
from functions.Mozartizer import Mozartizer
from helper import Sentence
from neocortex import memories
from neocortex.memories import valid_username

processed_inline_kudos = {}
log = logging.getLogger()


def create_reply_from(update: Update) -> List[InlineQueryResultArticle]:
    user_input = Sentence(update.inline_query.query)
    return create_results(user_input)


def generate_mozartized_article(query: Sentence):
    mozartized = Mozartizer(query).mozartize()
    if not mozartized:
        mozartized = 'Mnmnmnnn'

    return InlineQueryResultArticle(
        id=uuid4(),
        title="Mozartize",
        description="Get a mumbled version of your input.",
        input_message_content=InputTextMessageContent(mozartized))


def create_results(query: Sentence) -> List[InlineQueryResultArticle]:
    results = [generate_aehxtended_article(query), generate_mozartized_article(query)]
    kudos_article = generate_kudos_article(query)
    if kudos_article:
        results.append(kudos_article)
    return results


def generate_kudos_article(query: Sentence) -> Optional[InlineQueryResultArticle]:
    mentioned_users = [word[1:] for word in query.word_list if word.startswith("@") and valid_username(word[1:])]
    if not mentioned_users:
        return None
    user_names = ' '.join(mentioned_users)
    callback_key = uuid4()
    processed_inline_kudos[str(callback_key)] = mentioned_users
    return InlineQueryResultArticle(
        id=callback_key,
        title="Give Kudos",
        description=user_names,
        input_message_content=InputTextMessageContent(f"Gave kudos to {user_names}"))


def generate_aehxtended_article(query: Sentence) -> InlineQueryResultArticle:
    aehxtended = Aehxtender(query).get_aehxtended()
    if not aehxtended:
        aehxtended = 'äh'
    return InlineQueryResultArticle(
        id=uuid4(),
        title="Ähxtend",
        description="Ähxtends your sentence!",
        input_message_content=InputTextMessageContent(aehxtended))


def process_callback(update: Update):
    sender = memories.remember_telegram_user(update.effective_user)
    receivers = link_to_inline_result(update)
    for receiver in receivers:
        receiver = memories.remember_username(receiver)
        memories.give_kudos(sender, receiver)


def link_to_inline_result(update) -> List[str]:
    try:
        receivers = processed_inline_kudos[update.chosen_inline_result.result_id]
    except KeyError:
        log.info("Update couldn't be linked to sent inline response.")
        return []
    return receivers
