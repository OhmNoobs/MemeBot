import logging
from typing import List

from telegram import MessageEntity, Chat, Update
from neocortex import memories

log = logging.getLogger()
MENTION = MessageEntity.MENTION


class KudosMessageParser:

    def __init__(self, update: Update):
        self.update = update
        self.entities = update.message.entities  # type: MessageEntity
        self.chat = update.effective_chat  # type: Chat
        self.mentions = [item for item in self.entities if item.type == MENTION]  # type: List[MessageEntity]
        self.in_group_chat = self.chat.type == Chat.GROUP or self.chat.type == Chat.SUPERGROUP  # type: bool

    def book_kudos(self) -> str:
        sender = memories.remember_telegram_user(self.update.message.from_user)
        if not self.in_group_chat:
            return "Only works in (super)group chats."
        if not self.mentions:
            return "You need to [mention](https://telegram.org/blog/replies-mentions-hashtags#mentions) " \
                   "someone to give him kudos! If the mention is not resolved into a clickable link, you're " \
                   "doing it wrong!"
        mentioned_users = map(self.convert_to_memory_of_user, self.mentions)
        for mentioned_user in mentioned_users:
            memories.give_kudos(giver=sender, taker=mentioned_user)
        return "done."

    def convert_to_memory_of_user(self, mention: MessageEntity):
        telegram_user = mention.user
        if telegram_user:
            memorized_user = memories.remember_telegram_user(telegram_user)
        else:
            memorized_user = memories.remember_username(self.extract_username(mention))
        return memorized_user

    def extract_username(self, mention: MessageEntity):
        name_start = mention.offset + 1
        name_end = mention.offset + mention.length
        mentioned_user = self.update.message.text[name_start:name_end]
        return mentioned_user

