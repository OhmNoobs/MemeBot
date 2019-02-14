from common import START_HELP, VERSION


def greet_user(username) -> str:
    return f'Hello {username}'


def help_user(first_name) -> str:
    return f'Hi {first_name} here is what I can do: {START_HELP}.'


def version() -> str:
    return VERSION
