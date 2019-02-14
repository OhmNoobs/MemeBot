from common import chance_to_return_true, Sentence


class Mozartizer:

    def __init__(self, sentence: Sentence):
        self.sentence = sentence.word_list
        self.mozartized_sentence = []

    def mozartize(self) -> str:
        for word in self.sentence:
            self.mozartized_sentence.append(self._maybe_mozartize(word))
        return ' '.join(self.mozartized_sentence)

    def _maybe_mozartize(self, word: str) -> str:
        if chance_to_return_true():
            word = self.mozartize_word(word)
        return word

    @staticmethod
    def mozartize_word(word: str) -> str:
        mozartized_word = ''
        for _ in word:
            if chance_to_return_true():
                mozartized_word += 'n' if chance_to_return_true() else 'N'
            else:
                mozartized_word += 'M' if chance_to_return_true() else 'm'
        return mozartized_word
