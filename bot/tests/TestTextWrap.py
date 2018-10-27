import unittest

from functions.Exmatriculator import FONTS
from helper import text_wrap


class TestTextWrap(unittest.TestCase):

    empty_string = ""
    short_string = "abc def"
    medium_string = "a b c d e f g h i j k l M n O p Q r S t u F W x Y Z A B C D E F H I J K L M N O P Q"
    long_word = "ABCDEFGHIJKLMNOPQRSTUVXWZABCDEFGHIJKLMNOPQRSTUVXWZ"
    max_width = 568

    def test_empty(self):
        wrapped = text_wrap(self.empty_string, FONTS.hand_writing_small, self.max_width)
        self.assertEqual([self.empty_string], wrapped)

    def test_short(self):
        wrapped = text_wrap(self.short_string, FONTS.hand_writing_small, self.max_width)
        self.assertEqual([self.short_string], wrapped)

    def test_two_lines_long(self):
        # tests if two rows are produced from a string wider than one row but shorter than three
        wrapped = text_wrap(self.medium_string, FONTS.hand_writing_small, self.max_width)
        self.assertEqual(2, len(wrapped))

    def test_long_word(self):
        wrapped = text_wrap(self.long_word, FONTS.hand_writing_small, self.max_width)[0]
        self.assertEqual("... ", wrapped[-4:])
        self.assertTrue(FONTS.hand_writing_small.getsize(wrapped)[0] < self.max_width)

    def test_long_words(self):
        wrapped = text_wrap(self.long_word + " " + self.long_word, FONTS.hand_writing_small, self.max_width)
        self.assertEqual(2, len(wrapped))
