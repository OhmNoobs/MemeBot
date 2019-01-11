import logging
from typing import List

import telegram

from neocortex import memories
from neocortex.memories import User

log = logging.getLogger()


class KudosMessageParser:

    def __init__(self, update: telegram.Update):
        self.update = update
        self.entities = update.message.entities  # type: telegram.MessageEntity
        self.chat = update.effective_chat  # type: telegram.Chat
        self.raw_mentions = [item for item in self.entities if item.type == item.MENTION]  # type: List[telegram.MessageEntity]
        self.in_group_chat = self.chat.type == self.chat.GROUP or self.chat.type == self.chat.SUPERGROUP

    def book_kudos(self) -> str:
        sender = memories.remember_telegram_user(self.update.message.from_user)
        if not self.in_group_chat:
            return "Only works in (super)group chats."
        mentioned_users = map(func=self.convert_to_memory_of_user, iter1=self.raw_mentions)
        for mentioned_user in mentioned_users:
            memories.give_kudos(giver=sender, taker=mentioned_user)
        return "done."

    def convert_to_memory_of_user(self, mention: telegram.MessageEntity):
        telegram_user = mention.user  # type: telegram.User
        if telegram_user:
            receiver = memories.remember_telegram_user(telegram_user)
        else:
            receiver = self.remember_username(mention)
        return receiver

    def remember_username(self, mention: telegram.MessageEntity) -> User:
        name_start = mention.offset + 1
        name_end = mention.offset + mention.length
        mentioned_user = self.update.message.text[name_start:name_end]
        receiver = memories.get_user_by_username(mentioned_user)
        if not receiver:
            receiver = memories.add_user(mentioned_user)
        return receiver
