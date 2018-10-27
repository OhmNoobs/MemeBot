import io
import random
import string
import unittest

from functions import food_scraper
from functions.Aehxtender import Aehxtender
from functions.Exmatriculator import text_wrap, FONTS
from helper import Sentence, ROOT_DIR
from pathlib import Path

PATH_TO_RESOURCES = Path(ROOT_DIR) / "tests" / "resources"


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

    def test_end_of_word(self):
        aehxtender = Aehxtender(self.single_word)
        aehxtender.current_position = len(aehxtender.sentence)
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("word-äh", aehxtender.sentence)

    def test_double_aehxtension_at_end_of_word(self):
        aehxtender = Aehxtender(self.single_word)
        aehxtender.current_position = len(aehxtender.sentence)
        length_of_aehxtension = aehxtender.aehxtend_at_current_position()
        self.assertEqual(3, aehxtender.length_of_last_aehxtension, length_of_aehxtension)
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("word-äh", aehxtender.sentence)


class TestFoodScraper(unittest.TestCase):

    def test_cached_food_pages(self):
        cached_pages_paths = PATH_TO_RESOURCES.glob('food_page_*.txt')
        cached_results_paths = PATH_TO_RESOURCES.glob('parsed_food_page_*.txt')
        actual_results = self.fetch_actual_results(cached_pages_paths)
        expected_results = self.fetch_expected_results(cached_results_paths)
        for expected_result, actual_result in zip(expected_results, actual_results):
            self.assertEqual(expected_result, actual_result)

    @staticmethod
    def fetch_actual_results(cached_pages_paths):
        actual_results = []
        for path in cached_pages_paths:
            with io.open(str(path), mode="r", encoding="utf-8") as soup_file:
                soup = soup_file.read().replace('\r', '').replace('\n', '')
                meals = food_scraper.cook_meals(soup)
                feast = food_scraper.dish_up(meals)
                actual_results.append(feast)
        return actual_results

    @staticmethod
    def fetch_expected_results(cached_results_paths):
        expected_results = []
        for path in cached_results_paths:
            with io.open(str(path), mode="r", encoding="utf-8") as result_file:
                expected_results.append(result_file.read())
        return expected_results

