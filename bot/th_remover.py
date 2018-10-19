from datetime import date
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from typing import NamedTuple


class Arguments(NamedTuple):
    surname: str
    last_name: str
    reason: str


class TextFields(NamedTuple):
    reason_formatted: str
    date_numbers_long: str
    date_numbers_short: str
    date_formal: str
    first_and_last_name: str


class UsedFonts(NamedTuple):
    sans_serif: ImageFont.FreeTypeFont
    hand_writing: ImageFont.FreeTypeFont
    hand_writing_small: ImageFont.FreeTypeFont


def remove_from_th(bot, update, args) -> None:
    args = prepare_arguments(args)
    if args.surname == "":
        update.message.reply_text("Usage: /exmatrikulieren Vorname Nachname Grund bla bla bla")
        return

    image = compose_image(args)
    bio = get_as_bytes_io(image)
    bot.send_photo(update.message.chat_id, photo=bio)


def get_as_bytes_io(image):
    bio = BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'png')
    bio.seek(0)
    return bio


def compose_image(args):
    image = Image.open("removal_form.png")
    drawing = ImageDraw.Draw(image)
    fonts = define_fonts()
    text_fields = build_texts(args, fonts.hand_writing_small)
    draw_text(args, drawing, fonts, text_fields)
    return image


def draw_text(args, drawing, fonts, text_fields):
    drawing.text((120, 90), args.last_name, (0, 0, 0), font=fonts.sans_serif)
    drawing.text((420, 90), args.surname, (0, 0, 0), font=fonts.sans_serif)
    drawing.text((420, 210), text_fields.date_numbers_long, (0, 0, 0), font=fonts.sans_serif)
    drawing.text((170, 360), text_fields.date_numbers_short, (0, 0, 0), font=fonts.sans_serif)
    drawing.text((420, 759), text_fields.first_and_last_name, (0, 81, 158), font=fonts.hand_writing)
    drawing.text((40, 635), text_fields.reason_formatted, (0, 81, 158), font=fonts.hand_writing_small)
    drawing.text((40, 773), text_fields.date_formal, (0, 81, 158), font=fonts.hand_writing_small)


def define_fonts():
    sans_serif = ImageFont.truetype("Roboto-Regular.ttf", 16)
    hand_writing = ImageFont.truetype("DawningofaNewDay.ttf", 22)
    hand_writing_small = ImageFont.truetype("DawningofaNewDay.ttf", 18)
    return UsedFonts(sans_serif, hand_writing, hand_writing_small)


def build_texts(args, hand_writing_small):
    reason_multi_line = text_wrap(args.reason, hand_writing_small, 563)
    return TextFields(
        "\n".join(reason_multi_line[:2]),
        date.today().strftime("%d.%m.%Y"),
        date.today().strftime("%m/%Y"),
        "Nürnberg, " + date.today().strftime("%d. %B %Y"),
        f"{args.surname} {args.last_name}"
    )


def prepare_arguments(args):
    surname = ""
    last_name = ""
    reason = "Noob."
    if len(args) > 0:
        if len(args) > 0:
            surname = args[0].capitalize()
        if len(args) > 1:
            last_name = args[1].capitalize()
        if len(args) > 2:
            reason = " ".join(args[2:])
    return Arguments(surname, last_name, reason)


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