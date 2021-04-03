import logging
from multiprocessing import Pool
from collections import Counter
from time import time
from itertools import chain
from typing import List, Dict

import config
from parsers import get_next_pagination_url, get_animals
from utils import get_response, is_latin_letter


def count_data(animals: List[str]) -> Dict[str, int]:
    raw_data = dict(Counter(item[0] for item in animals))
    return {
        letter: raw_data[letter]
        for letter
        in config.LETTERS
    }


def normalize_data(raw_data: List[List[str]]) -> List[str]:
    data = list(chain.from_iterable(raw_data))
    unique_animals = list(set(data))
    return [
        i for i
        in unique_animals
        if not is_latin_letter(i)
    ]


def parse_data_multiprocess(letter: str):
    url = config.URL.format(letter=letter)
    logging.info(f'Letter - {letter}')
    last_letter = letter
    animals_data = []

    while letter == last_letter:
        response = get_response(url)

        if response.status_code != 200:
            response = get_response(url, from_captcha=True)

        url = config.BASE_URL + get_next_pagination_url(response.text)
        buffer = get_animals(response.text)
        last_letter = buffer[-1][0]
        animals_data.append(buffer)

    return list(chain.from_iterable(animals_data))


def main():
    logging.info('Start parsing')
    num_of_pools = len(config.LETTERS)

    t0 = time()
    with Pool(processes=num_of_pools) as pool:
        raw_data = pool.map(parse_data_multiprocess, config.LETTERS)
        animals = normalize_data(raw_data)
        print(animals)
        stats = count_data(animals)

        print('\n' * 2 + '_' * 80)
        for k, v in stats.items():
            print(f'{k}: {v}')

    t1 = time()
    logging.info('Parsing was completed')
    logging.info(f'Parse time: {t1 - t0}')


if __name__ == '__main__':
    log_format = '%(asctime)s - %(message)s'
    logging.basicConfig(format=log_format, datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    main()
