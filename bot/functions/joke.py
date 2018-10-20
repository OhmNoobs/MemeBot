import re
import requests
from typing import List

CHUCK_API = "https://api.chucknorris.io/jokes/random"
CHUCK = re.compile("chuck", re.IGNORECASE)
NORRIS = re.compile("norris", re.IGNORECASE)


def make_joke_about(args: List[str]) -> str:
    try:
        response = requests.get(CHUCK_API)
    except requests.exceptions.RequestException:
        response = None

    if response and response.json()["value"]:
        response = response.json()
        joke = response["value"]  # type: str
        if args:
            if len(args) > 0:
                joke = CHUCK.sub(args[0].capitalize(), joke)
            if len(args) > 1:
                joke = NORRIS.sub(args[1].capitalize(), joke)
    else:
        if args:
            joke_target = args.join(' ')
            joke = f"Da hat {joke_target} nochmal glück gehabt. Gibt grad keine Witze."
        else:
            joke = "Kein Witz :("
    return joke
