from helper import fortune_is_willing, Sentence


class Aehxtender:

    """Aehxtends a sentence by randomly adding äh's to it.

    This is achieved by iterating over the sentence letter by letter. Each character has a chance of spawning an
    aehxtension. Depending on the position in the sentence the aehxtension will be partially or fully padded by
    hyphens or not.
    """

    def __init__(self, sentence: Sentence):
        self.sentence = str(sentence)
        self.current_position = 0
        self.length_of_last_aehxtension = 0

    def get_aehxtended(self) -> str:
        while self.current_position < len(self.sentence):
            self.randomly_aehxtend()
        return self.sentence

    def randomly_aehxtend(self) -> None:
        if fortune_is_willing(probability=12):
            length_of_extension = self.aehxtend_at_current_position()
            self.current_position = self.current_position + length_of_extension
        else:
            self.current_position += 1

    def aehxtend_at_current_position(self) -> int:
        aehxtension = self.build_aehxtension()
        self.sentence = self.sentence[:self.current_position] + aehxtension + self.sentence[self.current_position:]
        return len(aehxtension)

    def build_aehxtension(self):
        pre_padding = self.decide_on_pre_padding()
        post_padding = self.decide_on_post_padding()
        return f"{pre_padding}äh{post_padding}"

    def decide_on_pre_padding(self) -> str:
        return '' if self.at_start_of_sentence() or self.at_beginning_of_word() or self.hyphen_before() else '-'

    def decide_on_post_padding(self) -> str:
        return '' if self.at_end_of_sentence() or self.at_end_of_word() or self.hyphen_after() else '-'

    def at_start_of_sentence(self) -> bool:
        return self.current_position == 0

    def at_beginning_of_word(self) -> bool:
        return self.sentence[self.current_position - 1] == ' '

    def hyphen_before(self) -> bool:
        return self.sentence[self.current_position - 1] == '-'

    def at_end_of_sentence(self) -> bool:
        return self.current_position == len(self.sentence)

    def at_end_of_word(self) -> bool:
        return self.sentence[self.current_position] == ' '

    def hyphen_after(self) -> bool:
        return self.sentence[self.current_position] == '-'
