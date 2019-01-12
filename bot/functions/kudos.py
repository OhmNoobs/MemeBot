import logging
from typing import List

from telegram import MessageEntity, Chat, Update, User, Message
from neocortex import memories

log = logging.getLogger()
MENTION = MessageEntity.MENTION
GROUP_CHAT_TYPES = [Chat.GROUP, Chat.SUPERGROUP]


class KudosMessageParser:

    def __init__(self, update: Update):
        self.message = update.message  # type: Message
        self.chat = update.effective_chat  # type: Chat
        self.mentions = [item for item in update.message.entities if item.type == MENTION]  # type: List[MessageEntity]
        self.in_group_chat = update.effective_chat.type in GROUP_CHAT_TYPES  # type: bool
        self.only_command_sent = self.message.text.strip() == '/kudos'

    def handle_kudos_command(self) -> str:
        sender = memories.remember_telegram_user(self.message.from_user)
        if not self.mentions:
            return self.no_mentions_reply()
        if not self.in_group_chat:
            return "Only works in (super)group chats."
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
        mentioned_user = self.message.text[name_start:name_end]
        return mentioned_user

    def no_mentions_reply(self):
        if not self.only_command_sent:
            # something followed the /kudos command that did not contain a mention
            return "You need to mention someone to give him kudos! If the mention is not resolved into a clickable " \
                   "link, you're doing it wrong!\n\nYou can send me /kudos (without args) to see the top 10. \n" \
                   "(https://telegram.org/blog/replies-mentions-hashtags#mentions)"
        else:
            # nothing followed the /kudos command: send top 10
            return memories.remember_top_n_kudos_receivers(10)

