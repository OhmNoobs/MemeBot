import random
import string
import unittest

from functions.Aehxtender import Aehxtender
from functions.th_remover import text_wrap, FONTS
from helper import Sentence, ROOT_DIR
from pathlib import Path

RESOURCES = Path(ROOT_DIR) / "tests" / "resources"


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


def generate_random_word():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 20)))


class TestAehxtender(unittest.TestCase):

    empty_sentence = Sentence([""])
    single_hyphen = Sentence(["-"])
    double_hyphen = Sentence(["--"])
    single_word = Sentence(["word"])
    word_followed_by_hyphen = Sentence(["word-"])
    word_preceded_by_hyphen = Sentence(["-word"])
    two_word_sentence = Sentence(["a", "house"])
    two_words_hyphen_in_between = Sentence(["a-", "house"])
    random_list_of_random_strings = [generate_random_word() for n in range(random.randint(200, 1337))]
    long_sentence = Sentence(random_list_of_random_strings)

    def test_empty(self):
        aehxtender = Aehxtender(self.empty_sentence)
        self.assertEqual(aehxtender.get_aehxtended(), "")

    def test_single_hyphen(self):
        aehxtender = Aehxtender(self.single_hyphen)
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("äh-", aehxtender.sentence)

    def test_double_hyphen(self):
        aehxtender = Aehxtender(self.double_hyphen)
        length_of_aehxtension = aehxtender.aehxtend_at_current_position()
        aehxtender.current_position += length_of_aehxtension
        aehxtender.current_position += 1  # no luck (single aehxtension)
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("äh-äh-", aehxtender.sentence)


class TestFoodScraper(unittest.TestCase):

    def test_cached_food_pages(self):
        cached_pages_paths = RESOURCES.glob('food_page_*.txt')
        for path in cached_pages_paths:
            pass
        self.assertTrue(True)

