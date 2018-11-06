from datetime import date
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from typing import NamedTuple, List, Optional
from pathlib import Path
from helper import text_wrap, ROOT_DIR


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


resources_path = Path(ROOT_DIR) / "resources"
PATH_TO_CANVAS_IMAGE = resources_path / "images" / "removal_form.png"
fonts_path = (resources_path / "fonts")
roboto_font_face = str(fonts_path / "Roboto-Regular.ttf")
dawning_of_a_new_day_font_face = str(fonts_path / "DawningofaNewDay.ttf")
FONTS = UsedFonts(
    ImageFont.truetype(roboto_font_face, 16),
    ImageFont.truetype(dawning_of_a_new_day_font_face, 22),
    ImageFont.truetype(dawning_of_a_new_day_font_face, 18)
)


def generate_exmatriculation(args) -> Optional[BytesIO]:
    args = prepare_arguments(args)
    if args.surname == "":
        return
    image = compose_image(args)
    bio = get_as_bytes_io(image)
    return bio


def prepare_arguments(args: List[str]) -> Arguments:
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


def compose_image(args: Arguments) -> Image.Image:
    image = Image.open(PATH_TO_CANVAS_IMAGE)
    drawing = ImageDraw.Draw(image)
    text_fields = build_texts(args)
    draw_text(args, drawing, text_fields)
    return image


def build_texts(args) -> TextFields:
    reason_multi_line = text_wrap(args.reason, FONTS.hand_writing_small, 563)
    return TextFields(
        "\n".join(reason_multi_line[:2]),
        date.today().strftime("%d.%m.%Y"),
        date.today().strftime("%m/%Y"),
        "Nürnberg, " + date.today().strftime("%d. %B %Y"),
        f"{args.surname} {args.last_name}"
    )


def draw_text(args, drawing, text_fields) -> None:
    drawing.text((120, 90), args.last_name, (0, 0, 0), font=FONTS.sans_serif)
    drawing.text((420, 90), args.surname, (0, 0, 0), font=FONTS.sans_serif)
    drawing.text((420, 210), text_fields.date_numbers_long, (0, 0, 0), font=FONTS.sans_serif)
    drawing.text((170, 360), text_fields.date_numbers_short, (0, 0, 0), font=FONTS.sans_serif)
    drawing.text((420, 759), text_fields.first_and_last_name, (0, 81, 158), font=FONTS.hand_writing)
    drawing.text((40, 635), text_fields.reason_formatted, (0, 81, 158), font=FONTS.hand_writing_small)
    drawing.text((40, 773), text_fields.date_formal, (0, 81, 158), font=FONTS.hand_writing_small)


def get_as_bytes_io(image) -> BytesIO:
    bio = BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'png')
    bio.seek(0)
    return bio


