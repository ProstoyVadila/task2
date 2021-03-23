import logging
from collections import Counter
from datetime import datetime
from itertools import chain
from typing import List, Dict

import config
from parsers import get_next_pagination_url, get_animals
from utils import get_response, is_latin_letter


def parse_data(start_url: str) -> List[List[str]]:
    t1 = datetime.now()
    animals = []
    last_animal = ''
    url = start_url

    while not is_latin_letter(last_animal):
        response = get_response(url)
        logging.info(f'response_status: {response.status_code}'
                     f'\nresponse_url: {response.url}')

        if response.status_code in {301, 302}:
            logging.info('Changing headers')
            response = get_response(url, from_captcha=True)

        url = config.BASE_URL + get_next_pagination_url(response.text)
        animals_buffer = get_animals(response.text)
        last_animal = animals_buffer[-1]

        logging.info(f'letter: {last_animal[0]} - '
                     f'buffer_len: {len(animals_buffer)}')

        animals.append(animals_buffer)

    t2 = datetime.now()
    logging.info(f'Parse time: {t2 - t1}')
    return animals


def count_data(animals: List[str]) -> dict:
    raw_data = dict(Counter(item[0] for item in animals))
    return {
        letter: raw_data[letter]
        for letter
        in config.LETTERS
    }


def main():
    logging.info('Start parsing')
    data = parse_data(config.URL)
    logging.info('Parsing was completed')

    animals_raw = list(chain.from_iterable(data))
    animals = [i for i in animals_raw if not is_latin_letter(i)]

    print(animals)
    print('\n' * 2)
    print('_' * 100)
    print('\n' * 2)

    stats = count_data(animals)
    for k, v in stats.items():
        print(f'{k}:  {v}')


if __name__ == '__main__':
    log_format = '%(asctime)s - %(message)s'
    logging.basicConfig(format=log_format, datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    main()
