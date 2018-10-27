import random
import string
import unittest

from functions.Aehxtender import Aehxtender
from helper import Sentence


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
        length_of_aehxtension = aehxtender.aehxtend_at_current_position()
        self.assertEqual(3, length_of_aehxtension)
        self.assertEqual("word-äh", aehxtender.sentence)

    def test_end_of_word_last_char_hyphen(self):
        aehxtender = Aehxtender(self.word_followed_by_hyphen)
        aehxtender.current_position = len(aehxtender.sentence)
        length_of_aehxtension = aehxtender.aehxtend_at_current_position()
        self.assertEqual(2, length_of_aehxtension)
        self.assertEqual("word-äh", aehxtender.sentence)

    def test_start_of_word_first_char_hyphen(self):
        aehxtender = Aehxtender(self.word_preceded_by_hyphen)
        length_of_aehxtension = aehxtender.aehxtend_at_current_position()
        self.assertEqual(2, length_of_aehxtension)
        self.assertEqual("äh-word", aehxtender.sentence)

    def test_double_aehxtension_at_end_of_word(self):
        aehxtender = Aehxtender(self.single_word)
        aehxtender.current_position = len(aehxtender.sentence)
        length_of_aehxtension = aehxtender.aehxtend_at_current_position()
        aehxtender.current_position += length_of_aehxtension
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("word-äh-äh", aehxtender.sentence)

    def test_aehxtension_after_hyphen(self):
        aehxtender = Aehxtender(self.word_preceded_by_hyphen)
        aehxtender.current_position = 1
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("-äh-word", aehxtender.sentence)

    def test_aehxtension_before_hyphen(self):
        aehxtender = Aehxtender(self.word_followed_by_hyphen)
        aehxtender.current_position = len(aehxtender.sentence) - 1
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("word-äh-", aehxtender.sentence)

    def test_aehxtension_between_words_on_space(self):
        aehxtender = Aehxtender(self.two_word_sentence)
        aehxtender.current_position = 1
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("a-äh house", aehxtender.sentence)

    def test_aehxtension_between_words_on_first_letter_of_second_word(self):
        aehxtender = Aehxtender(self.two_word_sentence)
        aehxtender.current_position = 2
        aehxtender.aehxtend_at_current_position()
        self.assertEqual("a äh-house", aehxtender.sentence)

    def test_aehxtension_on_long_input(self):
        aehxtender = Aehxtender(self.long_sentence)
        input_length = len(str(self.long_sentence))
        result = aehxtender.get_aehxtended()
        expected_number_of_aehxtensions = input_length * aehxtender.chance
        aehxtensions = result.count('äh')
        delta = input_length * aehxtender.chance * 0.2
        self.assertAlmostEqual(expected_number_of_aehxtensions, aehxtensions, delta=delta)

