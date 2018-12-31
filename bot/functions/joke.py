import re
import requests
from typing import List, Optional

CHUCK_API = "https://api.chucknorris.io/jokes/random"
CHUCK = re.compile("chuck", re.IGNORECASE)
NORRIS = re.compile("norris", re.IGNORECASE)


def make_joke_about(args: List[str]) -> str:
    chuck_joke = get_chuck_joke()
    joke = individualize(args, chuck_joke)
    return joke


def get_chuck_joke() -> Optional[str]:
    try:
        response = requests.request(method='GET', url=CHUCK_API, timeout=5)
        response = response.json()["value"]
    except requests.exceptions.Timeout:
        response = "Can't think of a new joke right now."
    except requests.exceptions.RequestException or KeyError:
        response = None
    return response


def individualize(args, joke):
    if joke and args:
        joke = replace_chuck_with_args(args, joke)
    elif args and not joke:
        joke_target = ' '.join(args)
        joke = f"Da hat {joke_target} nochmal glück gehabt. Gibt grad keine Witze."
    elif not args and not joke:
        joke = "Kein Witz :("
    return joke


def replace_chuck_with_args(args, joke):
    if len(args) > 0:
        joke = CHUCK.sub(args[0].capitalize(), joke)
    if len(args) > 1:
        joke = NORRIS.sub(args[1].capitalize(), joke)
    return joke
