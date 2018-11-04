import os
import random

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Sentence:

    def __init__(self, list_of_words):
        if type(list_of_words) == str:
            self.word_list = list_of_words.split(' ')
        else:
            self.word_list = list_of_words

    def __repr__(self):
        return ' '.join(self.word_list)


def fortune_is_willing(probability=0.5) -> bool:
    if 0 < probability > 1:
        raise ValueError("Choose a value between 0 and 1")
    probability *= 100
    return random.randrange(0, 100) < probability


def text_wrap(text, font, max_width):
    lines = [""]
    if font.getsize(text)[0] <= max_width:
        lines[-1] = text
    else:
        words = text.split(' ')
        for word in words:
            if font.getsize(word)[0] > max_width:
                # if the word is to large for a single line, truncate until it fits.
                while font.getsize(word + "...")[0] > max_width:
                    word = word[:-1]
                word = word + "..."
            if font.getsize(lines[-1] + word)[0] <= max_width:
                # append word to last line
                lines[-1] = lines[-1] + word + " "
            else:
                # when the line gets longer than the max width append it to new line.
                lines.append(word + " ")
    return lines
