import logging
from typing import List

from telegram import MessageEntity, Chat, Update, Message
from neocortex import memories
from neocortex.memories import TopKudosReceiver

log = logging.getLogger()
MENTION = MessageEntity.MENTION
GROUP_CHAT_TYPES = [Chat.GROUP, Chat.SUPERGROUP]


class KudosMessageParser:

    def __init__(self, update: Update):
        self.update = update
        self.message = update.message  # type: Message
        self.chat = update.effective_chat  # type: Chat

    def handle_kudos_command(self) -> str:
        sender = memories.remember_telegram_user(self.message.from_user)
        mentions = [item for item in self.message.entities if item.type == MENTION]  # type: List[MessageEntity]
        if not mentions:
            return self._no_mentions_reply()
        if self.update.effective_chat.type not in GROUP_CHAT_TYPES:
            return "Only works in (super)group chats."
        mentioned_users = map(self._convert_to_memory_of_user, mentions)
        for mentioned_user in mentioned_users:
            memories.give_kudos(giver=sender, taker=mentioned_user)
        return "done."

    def _convert_to_memory_of_user(self, mention: MessageEntity):
        telegram_user = mention.user
        if telegram_user:
            memorized_user = memories.remember_telegram_user(telegram_user)
        else:
            memorized_user = memories.remember_username(self._extract_username(mention))
        return memorized_user

    def _extract_username(self, mention: MessageEntity):
        name_start = mention.offset + 1
        name_end = mention.offset + mention.length
        return self.message.text[name_start:name_end]

    def _no_mentions_reply(self):
        if not self.message.text.strip() == '/kudos':
            # something followed the /kudos command that did not contain a mention
            return "You need to mention someone with a username (@name) to give him kudos!"
        else:
            # nothing followed the /kudos command: send top 10
            top_receivers = memories.remember_top_n_kudos_receivers(10)
            return self.formulate_top_kudos_receivers_response(top_receivers)

    @staticmethod
    def formulate_top_kudos_receivers_response(top_receivers: List[TopKudosReceiver]) -> str:
        if not top_receivers:
            return "No kudos given so far. Start by sending `/kudos @user`"
        answer = f"Top {len(top_receivers)} good people:\n"
        for position, receiver in enumerate(top_receivers, 1):
            if receiver.kudos_received > 0:
                answer += f"{position}. {receiver.name} ({receiver.kudos_received} kudos received)\n"
        return answer
