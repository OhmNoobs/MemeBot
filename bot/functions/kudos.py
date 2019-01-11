import logging
from typing import List

import telegram

from neocortex import memories
from neocortex.memories import User

log = logging.getLogger()


class KudosMessageParser:

    def __init__(self, update: telegram.Update):
        self.update = update

    def book_kudos(self) -> str:
        sender = self.remember_user_from_telegram_user(self.update.message.from_user)
        entities = self.update.message.entities  # type: telegram.MessageEntity
        chat = self.update.effective_chat  # type: telegram.Chat
        mentions = [item for item in entities if item.type == item.MENTION]  # type: List[telegram.MessageEntity]
        if chat.type == chat.GROUP or chat.type == chat.SUPERGROUP:
            mentioned_users = self.process_mentions(mentions)
            for mentioned_user in mentioned_users:
                memories.give_kudos(giver=sender, taker=mentioned_user)
            return "done."
        else:
            return "Only works in (super) group chats."

    def process_mentions(self, mentions) -> List[User]:
        mentioned_users = []
        for mention in mentions:
            receiver = self.convert_to_memory_of_user(mention)
            mentioned_users.append(receiver)
        return mentioned_users

    def convert_to_memory_of_user(self, mention: telegram.MessageEntity):
        telegram_user = mention.user  # type: telegram.User
        if telegram_user:
            receiver = self.remember_user_from_telegram_user(telegram_user)
        else:
            receiver = self.remember_user_from_username(mention)
        return receiver

    def remember_user_from_username(self, mention):
        name_start = mention.offset + 1
        name_end = mention.offset + mention.length
        mentioned_user = self.update.message.text[name_start:name_end]
        receiver = memories.get_user_by_username(mentioned_user)
        if not receiver:
            receiver = memories.add_user(mentioned_user)
        return receiver

    @staticmethod
    def remember_user_from_telegram_user(full_user_reference) -> User:
        user = memories.get_user(full_user_reference.id)
        if not user:  # create one
            log.info(f'User {full_user_reference.username} unknown. Adding him now.')
            user = memories.add_telegram_user(full_user_reference)
        return user
