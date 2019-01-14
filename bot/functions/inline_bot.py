from typing import List
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update

from functions.Aehxtender import Aehxtender
from functions.Mozartizer import Mozartizer
from helper import Sentence
from neocortex import memories
from neocortex.memories import valid_username

processed_inline_kudos = {}


def create_reply_from(update: Update) -> List[InlineQueryResultArticle]:
    user_input = Sentence(update.inline_query.query)
    return create_results(user_input)


def create_results(query: Sentence) -> List[InlineQueryResultArticle]:
    results = []

    aehxtended = Aehxtender(query).get_aehxtended()
    if not aehxtended:
        aehxtended = 'äh'

    results.append(InlineQueryResultArticle(
        id=uuid4(),
        title="Ähxtend",
        description="Ähxtends your sentence!",
        input_message_content=InputTextMessageContent(aehxtended)))

    mozartized = Mozartizer(query).mozartize()
    if not mozartized:
        mozartized = 'Mnmnmnnn'

    results.append(InlineQueryResultArticle(
        id=uuid4(),
        title="Mozartize",
        description="Get a mumbled version of your input.",
        input_message_content=InputTextMessageContent(mozartized)))

    mentioned_users = [word for word in query.word_list if word.startswith("@") and valid_username(word[1:])]
    user_names = ' '.join(mentioned_users)
    if mentioned_users:
        callback_key = uuid4()
        processed_inline_kudos[str(callback_key)] = mentioned_users
        results.append(InlineQueryResultArticle(
            id=callback_key,
            title="Give Kudos",
            description=user_names,
            input_message_content=InputTextMessageContent(f"Gave kudos to {user_names}")))
    return results


def process_callback(update: Update):
    sender = memories.remember_telegram_user(update.effective_user)
    receivers = processed_inline_kudos[update.chosen_inline_result.result_id]
    for receiver in receivers:
        receiver = memories.remember_username(receiver[1:])
        memories.give_kudos(sender, receiver)
