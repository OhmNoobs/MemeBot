import unittest

from functions.ToiletPaper import ToiletPaper


class TestToiletPaper(unittest.TestCase):

    empty_string = [""]
    two_rows_multi_char_emoji = ["🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️"]
    one_row_multi_char_emoji = ["🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️"]
    mixed_content = ["a", "🤷"]

    def test_empty(self):
        wrapped = ToiletPaper(self.empty_string).wrap()
        self.assertEqual("🧻🧻🧻\n🧻🧻🧻\n🧻🧻🧻", wrapped)

    def test_two_rows_special(self):
        wrapped = ToiletPaper(self.two_rows_multi_char_emoji).wrap()
        self.assertEqual("🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻\n"
                         "🧻🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🧻\n"
                         "🧻🤷‍♂️🤷‍♂️🤷‍♂️🧻🧻🧻🧻🧻🧻🧻🧻\n"
                         "🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻", wrapped)

    def test_one_row_special(self):
        wrapped = ToiletPaper(self.one_row_multi_char_emoji).wrap()
        self.assertEqual("🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻\n"
                         "🧻🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🧻\n"
                         "🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻🧻", wrapped)
