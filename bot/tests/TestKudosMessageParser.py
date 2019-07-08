import datetime
import random
from typing import List
from unittest import TestCase

import telegram
from telegram import Update, Message, Chat, MessageEntity

from functions import KudosMessageParser
from neocortex import memories
from tests.test import mock_telegram_user


def random_id():
    return random.randint(1, 1337)


def mock_parser(sender_name: str, chat_type: str, text_to_parse: str, entities: List[telegram.MessageEntity] = None):
    sender_name = mock_telegram_user(sender_name)
    chat = Chat(random_id(), chat_type)
    message = Message(message_id=random_id(),
                      from_user=sender_name,
                      date=datetime.datetime.now(),
                      chat=chat,
                      text=text_to_parse,
                      entities=entities)
    update = Update(update_id=random_id(),
                    message=message,
                    effective_chat=chat)
    parser = KudosMessageParser(update)
    return parser


class TestKudosMessageParser(TestCase):

    def test__extract_username(self):
        parser = mock_parser(sender_name="joe",
                             chat_type=Chat.GROUP,
                             text_to_parse="/kudos @username")
        mention = MessageEntity(MessageEntity.MENTION, 7, 9)
        self.assertEqual("username", parser._extract_username(mention))

    def test__convert_to_memory_of_user(self):
        parser = mock_parser(sender_name="test_sender",
                             chat_type=Chat.GROUP,
                             text_to_parse="/kudos @username")
        parser._convert_to_memory_of_user(MessageEntity(MessageEntity.MENTION, 7, 9))
        self.assertEqual(memories._get_user_by_username("username").username, "username")

    def test__no_mentions_reply(self):
        argument = "asd"
        parser_with_invalid_argument = mock_parser(sender_name="test_sender",
                                                   chat_type=Chat.GROUP,
                                                   text_to_parse=f"/kudos {argument}")
        decoration = parser_with_invalid_argument.INVALID_ARGUMENTS_REPLY_DECORATION
        self.assertEqual(parser_with_invalid_argument._no_mentions_reply(), decoration + argument + decoration)

    def test__give_kudos_to_all_mentioned_users(self):
        username_1 = "user1"
        username_2 = "user2"
        parser = mock_parser(sender_name="test_sender",
                             chat_type=Chat.GROUP,
                             text_to_parse=f"/kudos @{username_1} @{username_2}",
                             entities=[MessageEntity(MessageEntity.MENTION, 7, 6),
                                       MessageEntity(MessageEntity.MENTION, 14, 6)])
        sender = memories.remember_telegram_user(parser.message.from_user)
        self.assertEqual('done.', parser._give_kudos_to_all_mentioned_users(sender))
        self.assertEqual(1, memories.get_kudos_of_user(memories._get_user_by_username(username_1)))
        self.assertEqual(1, memories.get_kudos_of_user(memories._get_user_by_username(username_2)))

    def test_handle_kudos_command(self):
        username_1 = "user8"
        username_2 = "user9"
        parser = mock_parser(sender_name="test_sender",
                             chat_type=Chat.GROUP,
                             text_to_parse=f"/kudos @{username_1} @{username_2}",
                             entities=[MessageEntity(MessageEntity.MENTION, 7, 6),
                                       MessageEntity(MessageEntity.MENTION, 14, 6)])
        self.assertEqual('done.', parser.handle_kudos_command())
        self.assertEqual(1, memories.get_kudos_of_user(memories._get_user_by_username(username_1)))
        self.assertEqual(1, memories.get_kudos_of_user(memories._get_user_by_username(username_2)))
