from helper import fortune_is_willing
from typing import List


class Aehxtender:

    def __init__(self, arguments: List[str]):
        self.sentence = ' '.join(arguments)
        self.current_position = 0

    def get_aehxtended(self) -> str:
        while self.current_position < len(self.sentence):
            self.randomly_aehxtend()
        return self.sentence

    def randomly_aehxtend(self) -> None:
        if fortune_is_willing(12):
            self.aehxtend_at_current_position()
            self.current_position = self.current_position + 4  # length of one aehxtension
        else:
            self.current_position += 1

    def aehxtend_at_current_position(self) -> None:
        pre_padding = self.decide_on_pre_padding()
        post_padding = self.decide_on_post_padding()
        aehxtension = f"{pre_padding}äh{post_padding}"
        self.sentence = self.sentence[:self.current_position] + aehxtension + self.sentence[self.current_position:]

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
