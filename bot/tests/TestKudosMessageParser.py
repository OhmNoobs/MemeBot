import datetime
import random
from unittest import TestCase

from telegram import Update, Message, User, Chat, MessageEntity

from functions import KudosMessageParser


def random_id():
    return random.randint(1, 1337)


def mock_parser(sender_name: str, chat_type: str, text_to_parse: str):
    sender_name = User(random_id(), sender_name, False)
    chat = Chat(random_id(), chat_type)
    message = Message(message_id=random_id(),
                      from_user=sender_name,
                      date=datetime.datetime.now(),
                      chat=chat,
                      text=text_to_parse)
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

    def test_handle_kudos_command(self):
        self.fail()

    def test__give_kudos_to_all_mentioned_users(self):
        self.fail()

    def test__no_mentions_reply(self):
        self.fail()
