from helper import fortune_is_willing, Sentence


class Mozartizer:

    def __init__(self, sentence: Sentence):
        self.sentence = str(sentence)
        self.mozartized_sentence = []

    def mozartize(self) -> str:
        for word in self.sentence:
            self.mozartized_sentence.append(self._maybe_mozartize(word))
        return ' '.join(self.mozartized_sentence)

    def _maybe_mozartize(self, word: str) -> str:
        if fortune_is_willing():
            word = self.mozartize_word(word)
        return word

    @staticmethod
    def mozartize_word(word: str) -> str:
        mozartized_word = ''
        for _ in word:
            if fortune_is_willing():
                mozartized_word += 'n' if fortune_is_willing() else 'N'
            else:
                mozartized_word += 'M' if fortune_is_willing() else 'm'
        return mozartized_word
