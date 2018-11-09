from typing import List

import requests
import re
import logging

from exceptions import ConnectionProblem, ParsingError, FoodProcessorError

log = logging.getLogger('')
URL = 'http://www.werkswelt.de/?id=hohf'
NEW_LINE_SEPARATOR = "\n\n"
PLAN_PATTERN = re.compile("Speiseplan.*<form", re.MULTILINE)
MEAL_PATTERN = re.compile("Essen (?P<meal_number>\d)</br>(((?P<meal_name>.*?)</br>)|(</br>))(?P<meal_price_student>.*?)&nbsp;.*?</br>((?P<meal_image_tags><img.*?>)</br>|)")
PARSING_ERROR_MESSAGE = "Can't extract meals section from mensa website."
DECORATION_INSTRUCTIONS = [
    ("_", "\\_"),
    ("*", "\\*"),
    ("`", "\\`"),
    ('<sup><b>', '_'),
    ('</b></sup>', '_')
]


def order() -> str:
    try:
        reply = make_meal()
    except FoodProcessorError as error:
        reply = str(error).replace('Döner', '[Döner](https://www.google.de/search?q=döner+sulzbacher+str.+nürnberg)')
    return reply


def make_meal() -> str:
    soup = make_soup()
    try:
        food = cook_meals(soup)
        return dish_up(food)
    except ParsingError:
        raise FoodProcessorError("Zum Glück gibt's immer Döner...")


def make_soup() -> str:
    try:
        soup = fetch_soup()
    except ConnectionError as connection_error:
        log.error(connection_error)
        raise ConnectionProblem("(ConnectionError) Ich kann den Koch nicht erreichen...")
    except requests.exceptions.HTTPError as http_error:
        log.error(http_error)
        raise Exception("(HTTPError) Ich kann den Koch nicht verstehen... "
                        "Hier ein bisschen shame 🔔, shame 🔔, shame 🔔 https://www.infomax.de/")
    except requests.exceptions.Timeout as timeout:
        log.error(timeout)
        raise ConnectionProblem("(Timeout) Das dauert zu lange... Hol dir nen Döner.")
    except requests.exceptions.TooManyRedirects as too_many_redirects:
        log.error(too_many_redirects)
        raise ConnectionProblem("(TooManyRedirects) Ach https://www.infomax.de/ ...")
    return soup


def fetch_soup() -> str:
    page = requests.get(URL)
    soup = page.text
    soup = soup.replace('\r', '').replace('\n', '')
    return soup


def cook_meals(soup: str) -> List[dict]:
    # throws attribute error if nothing found, slices out the relevant html
    match = PLAN_PATTERN.search(soup)
    if match:
        soup = match.group(0)
        return [m.groupdict() for m in MEAL_PATTERN.finditer(soup)]
    else:
        log.error(PARSING_ERROR_MESSAGE)
        raise ParsingError(PARSING_ERROR_MESSAGE)


def dish_up(food: List[dict]) -> str:
    feast = ""
    for meal in food:
        meal_name = decorate_platter(meal['meal_name'])
        feast += f"{meal['meal_number']}. {meal_name} *{meal['meal_price_student']}*{NEW_LINE_SEPARATOR}"
    return feast[:-len(NEW_LINE_SEPARATOR)]


def decorate_platter(meal: str) -> str:
    for decoration_instruction in DECORATION_INSTRUCTIONS:
        meal = meal.replace(*decoration_instruction)
    return meal


if __name__ == '__main__':
    print(order())
