import random
from string import ascii_letters
from time import sleep

import requests
from requests import Response

from config import HEADERS


def get_response(url: str, from_captcha: bool = False) -> Response:
    headers = None
    if from_captcha:
        headers = get_headers()
        sleep(random.uniform(0.1, 1))

    return requests.get(url=url, headers=headers)


def get_headers() -> dict[str, str]:
    user_agent = random.choice(HEADERS)
    return {
        'user-agent': user_agent
    }


def is_latin_letter(last_animal: str) -> bool:
    return any(letter in ascii_letters for letter in last_animal)
