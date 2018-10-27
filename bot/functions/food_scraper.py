import requests
import re
import logging

log = logging.getLogger('')
URL = 'http://www.werkswelt.de/?id=hohf'
NEW_LINE_SEPARATOR = "\n\n"
PLAN_MATCHER = re.compile("Speiseplan.*<form", re.MULTILINE)


def fetch_soup() -> list:
    page = requests.get(URL)
    soup = page.text
    soup = soup.replace('\r', '').replace('\n', '')
    return soup


def cook_meals(haystack):
    # throws attribute error if nothing found, slices out the relevant html
    haystack = PLAN_MATCHER.search(haystack).group(0)
    # Get food 1
    pattern = re.compile(
        "Essen (?P<meal_number>\d)</br>"
        "(((?P<meal_name>.*?)</br>)|(</br>))"
        "(?P<meal_price_student>.*?)&nbsp;.*?</br>"
        "((?P<meal_image_tags><img.*?>)</br>|.*?</br>)")
    matches = pattern.findall(haystack)
    return matches


def dish_up(food) -> str:
    feast = ""
    for meal in food:
        meal_name = meal.group('meal_name').replace('<sup><b>', '_').replace('</b></sup>', '_')
        feast += f"{meal.group('meal_number')}. {meal_name} *{meal.group('meal_price_student')}*{NEW_LINE_SEPARATOR}"
    return feast[:-len(NEW_LINE_SEPARATOR)]


def serve() -> str:
    error = False
    try:
        soup = fetch_soup()
    except ConnectionError:
        error = "(ConnectionError) Ich kann den Koch nicht erreichen..."
    except requests.exceptions.HTTPError:
        error = "(HTTPError) Ich kann den Koch nicht verstehen... " \
                "Hier ein bisschen shame 🔔, shame 🔔, shame 🔔 https://www.infomax.de/"
    except requests.exceptions.Timeout:
        error = "(Timeout) Das dauert zu lange... Hol dir nen Döner."
    except requests.exceptions.TooManyRedirects:
        error = "(TooManyRedirects) Ach https://www.infomax.de/ ..."
    if error:
        return error
    try:
        food = cook_meals(soup)
    except AttributeError as food_unmatched:
        log.error(food_unmatched)
        return "Zum Glück gibt's immer Döner..."
    return dish_up(food)


if __name__ == '__main__':
    print(serve())
