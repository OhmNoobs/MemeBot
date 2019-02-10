import logging
from typing import List

from telegram import MessageEntity, Chat, Update, Message

import neocortex
from neocortex import memories
from neocortex.memories import TopKudosReceiver

log = logging.getLogger()
MENTION = MessageEntity.MENTION
GROUP_CHAT_TYPES = [Chat.GROUP, Chat.SUPERGROUP]


def book_kudos(sender: neocortex.User, mentioned_users: List[neocortex.User]):
    for mentioned_user in mentioned_users:
        memories.give_kudos(giver=sender, taker=mentioned_user)


def formulate_top_kudos_receivers_response(top_receivers: List[TopKudosReceiver]) -> str:
    if not top_receivers:
        answer = "No kudos given so far. Start by sending `/kudos @user`"
    else:
        answer = f"Top {len(top_receivers)} good people:\n"
        for position, receiver in enumerate(top_receivers, 1):
            answer += f"{position}. {receiver.name} ({receiver.kudos_received} kudos received)\n"
    return answer


class KudosMessageParser:

    INVALID_ARGUMENTS_REPLY_DECORATION = "🙏🙏🙏"
    CHAT_TYPE_NOT_SUPPORTED_REPLY = "Only works in (super)group chats."

    def __init__(self, update: Update):
        if not type(update) == Update:
            raise ValueError("Only telegram.updates allowed.")
        self.update = update
        self.message = update.message  # type: Message
        self.chat = update.effective_chat  # type: Chat
        self.mentions = [item for item in update.message.entities if item.type == MENTION]  # type: List[MessageEntity]

    def handle_kudos_command(self) -> str:
        sender = memories.remember_telegram_user(self.message.from_user)
        if not self.mentions:
            answer = self._no_mentions_reply()
        elif self.update.effective_chat.type not in GROUP_CHAT_TYPES:
            answer = self.CHAT_TYPE_NOT_SUPPORTED_REPLY
        else:
            answer = self._give_kudos_to_all_mentioned_users(sender)
        return answer

    def _give_kudos_to_all_mentioned_users(self, sender: neocortex.User):
        mentioned_users = [self._convert_to_memory_of_user(mentioned_user) for mentioned_user in self.mentions]
        book_kudos(sender, mentioned_users)
        return "done."

    def _no_mentions_reply(self) -> str:
        if self.message.text.strip() == '/kudos':
            # nothing followed the /kudos command: send top 10
            top_receivers = memories.remember_top_n_kudos_receivers(10)
            return formulate_top_kudos_receivers_response(top_receivers)
        else:
            # something followed the /kudos command that did not contain a mention
            arguments = self.message.text[7:]
            return self.INVALID_ARGUMENTS_REPLY_DECORATION + arguments + self.INVALID_ARGUMENTS_REPLY_DECORATION

    def _convert_to_memory_of_user(self, mention: MessageEntity):
        username = self._extract_username(mention)
        return memories.remember_username(username)

    def _extract_username(self, mention: MessageEntity):
        return self.message.parse_entity(mention)[1:]
