import requests
import re

URL = 'http://www.werkswelt.de/?id=hohf'
NEW_LINE_SEPARATOR = "\n\n"


def fetch_food() -> list:

    page = requests.get(URL)
    haystack = page.text

    # Get food 1
    pattern = re.compile("Speiseplan <br><h4>(.*?)</h4>Essen (?P<meal_number>\d)</br>(((?P<meal_name>.*?)</br>)|(</br>))(?P<meal_price_student>.*?)&nbsp;.*?</br>((?P<meal_image_tags><img.*?>)</br>|.*?</br>)")
    match1 = pattern.search(haystack)
    found_food_1 = match1.group()
    split_pos = haystack.find(found_food_1)
    haystack = haystack[split_pos+len(found_food_1):]

    # Get food 2
    pattern = re.compile("Essen (?P<meal_number>\d)</br>(((?P<meal_name>.*?)</br>)|(</br>))(?P<meal_price_student>.*?)&nbsp;.*?</br>((?P<meal_image_tags><img.*?>)</br>|.*?</br>)")
    match2 = pattern.search(haystack)
    return [match1, match2]


def dish_up(food) -> str:
    if not food:
        return "Zum Glück gibts auch Döner..."
    feast = ""
    for meal in food:
        meal_name = meal.group('meal_name').replace('<sup><b>', '_').replace('</b></sup>', '_')
        feast += f"{meal.group('meal_number')}. {meal_name} *{meal.group('meal_price_student')}*{NEW_LINE_SEPARATOR}"
    return feast[:-len(NEW_LINE_SEPARATOR)]


def serve() -> str:
    return dish_up(fetch_food())


if __name__ == '__main__':
    print(serve())
    pass
