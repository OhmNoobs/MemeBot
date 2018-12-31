from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent

from functions.Aehxtender import Aehxtender
from functions.Mozartizer import Mozartizer
from helper import Sentence


def process(update):
    aehxtended, mozartized = create_results(update.inline_query.query)
    return provide_results(aehxtended, mozartized)


def provide_results(aehxtended, mozartized):
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


def create_results(query):
    aehxtended = Aehxtender(Sentence(query)).get_aehxtended()
    if not aehxtended:
        aehxtended = 'äh'
    mozartized = Mozartizer(Sentence(query)).mozartize()
    if not mozartized:
        mozartized = 'Mnmnmnnn'
    return aehxtended, mozartized
