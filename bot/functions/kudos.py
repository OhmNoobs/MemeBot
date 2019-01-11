from typing import List

import telegram

from neocortex import memories


def book_kudos(update: telegram.Update) -> str:
    sender = update.message.from_user  # type: telegram.User
    entities = update.message.entities  # type: telegram.MessageEntity
    chat = update.effective_chat  # type: telegram.Chat
    mentions = [item for item in entities if item.type == item.MENTION]  # type: List[telegram.MessageEntity]

    for mention in mentions:
        mentioned_user = update.message.text[mention.offset+1:mention.offset+mention.length]
        # TODO: check if user mentions self.
        if chat.type == chat.GROUP or chat.type == chat.SUPERGROUP:
            # handles groups
            pass
        else:
            return "Only works in (super) group chats."
        # memories.give_kudos(sender, mention.user)
    return "done."
