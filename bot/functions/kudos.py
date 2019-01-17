import logging
from typing import List

from telegram import MessageEntity, Chat, Update, Message
from neocortex import memories, User
from neocortex.memories import TopKudosReceiver

log = logging.getLogger()
MENTION = MessageEntity.MENTION
GROUP_CHAT_TYPES = [Chat.GROUP, Chat.SUPERGROUP]


def book_kudos(sender: User, mentioned_users: List[User]):
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

    def __init__(self, update: Update):
        self.update = update
        self.message = update.message  # type: Message
        self.chat = update.effective_chat  # type: Chat
        self.mentions = [item for item in update.message.entities if item.type == MENTION]  # type: List[MessageEntity]

    def handle_kudos_command(self) -> str:
        sender = memories.remember_telegram_user(self.message.from_user)
        if not self.mentions:
            answer = self._no_mentions_reply()
        elif self.update.effective_chat.type not in GROUP_CHAT_TYPES:
            answer = "Only works in (super)group chats."
        else:
            answer = self._give_kudos_to_all_mentioned_users(sender)
        return answer

    def _give_kudos_to_all_mentioned_users(self, sender: User):
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
            return "You need to mention someone with a username (@name) to give him kudos!"

    def _convert_to_memory_of_user(self, mention: MessageEntity):
        username = self._extract_username(mention)
        return memories.remember_username(username)

    def _extract_username(self, mention: MessageEntity):
        name_start = mention.offset + 1
        name_end = mention.offset + mention.length
        return self.message.text[name_start:name_end]
