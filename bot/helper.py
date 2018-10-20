import random


def fortune_is_willing(percent=50) -> bool:
    return random.randrange(0, 100) < percent


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
