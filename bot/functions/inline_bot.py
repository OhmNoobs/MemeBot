from typing import List
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update

from functions.Aehxtender import Aehxtender
from functions.Mozartizer import Mozartizer
from helper import Sentence


def process(update: Update) -> List[InlineQueryResultArticle]:
    user_input = Sentence(update.inline_query.query)
    aehxtended, mozartized = create_results(user_input)
    return provide_results(aehxtended, mozartized)


def provide_results(aehxtended: str, mozartized: str) -> List[InlineQueryResultArticle]:
    aehxtended_result = InlineQueryResultArticle(
        id=uuid4(),
        title="Ähxtend",
        description="Ähxtends your sentence!",
        input_message_content=InputTextMessageContent(aehxtended))
    mozartized_result = InlineQueryResultArticle(
        id=uuid4(),
        title="Mozartize",
        description="Get a mumbled version of your input.",
        input_message_content=InputTextMessageContent(mozartized))
    return [aehxtended_result, mozartized_result]


def create_results(query: Sentence):
    aehxtended = Aehxtender(query).get_aehxtended()
    if not aehxtended:
        aehxtended = 'äh'
    mozartized = Mozartizer(query).mozartize()
    if not mozartized:
        mozartized = 'Mnmnmnnn'
    return aehxtended, mozartized
