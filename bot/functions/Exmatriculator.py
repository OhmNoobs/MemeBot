from datetime import date
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from typing import NamedTuple, List, Optional
from pathlib import Path
from helper import text_wrap, ROOT_DIR


class ExmatriculationInformation(NamedTuple):
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


class Exmatriculation(NamedTuple):
    form: BytesIO
    description: str


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


def generate_exmatriculation(arguments) -> Optional[Exmatriculation]:
    arguments = parse_input(arguments)
    if not arguments:
        return None
    image = compose_image(arguments)
    bio = get_as_bytes_io(image)
    return Exmatriculation(form=bio, description=f"Exmatrikulation für {arguments.surname} {arguments.last_name}")


def parse_input(args: List[str]) -> Optional[ExmatriculationInformation]:
    if len(args) > 0:
        last_name = ""
        reason = "Noob."
        surname = args[0].capitalize()
        if len(args) > 1:
            last_name = args[1].capitalize()
        if len(args) > 2:
            reason = " ".join(args[2:])
        return ExmatriculationInformation(surname, last_name, reason)
    else:
        return None


def compose_image(details: ExmatriculationInformation) -> Image.Image:
    image = Image.open(PATH_TO_CANVAS_IMAGE)
    drawing = ImageDraw.Draw(image)
    text_fields = build_texts(details)
    draw_text(details, drawing, text_fields)
    return image


def build_texts(details) -> TextFields:
    reason_multi_line = text_wrap(details.reason, FONTS.hand_writing_small, 563)
    return TextFields(
        reason_formatted="\n".join(reason_multi_line[:2]),
        date_numbers_long=date.today().strftime("%d.%m.%Y"),
        date_numbers_short=date.today().strftime("%m/%Y"),
        date_formal="Nürnberg, " + date.today().strftime("%d. %B %Y"),
        first_and_last_name=f"{details.surname} {details.last_name}"
    )


def draw_text(details, drawing, text_fields) -> None:
    drawing.text((120, 90), details.last_name, (0, 0, 0), font=FONTS.sans_serif)
    drawing.text((420, 90), details.surname, (0, 0, 0), font=FONTS.sans_serif)
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


