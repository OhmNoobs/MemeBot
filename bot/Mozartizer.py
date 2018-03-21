from bot import helper
from typing import List


class Mozartizer:

    def __init__(self, sentence: List[str]):
        self.sentence = sentence
        self.mozartized_sentence = []

    def mozartize(self) -> str:
        for word in self.sentence:
            self.mozartized_sentence.append(self._maybe_mozartize(word))
        return ' '.join(self.mozartized_sentence)

    def _maybe_mozartize(self, word):
        if helper.fortune_is_willing():
            word = self.mozartize_word(word)
        return word

    @staticmethod
    def mozartize_word(word: str) -> str:
        mozartized_word = ''
        for _ in word:
            if helper.fortune_is_willing():
                mozartized_word += 'n' if helper.fortune_is_willing() else 'N'
            else:
                mozartized_word += 'M' if helper.fortune_is_willing() else 'm'
        return mozartized_word
