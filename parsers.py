from typing import List

from bs4 import BeautifulSoup


def get_next_pagination_url(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find(id='mw-pages')
    try:
        return div.find('a', title=True, text='Следующая страница').get('href')
    except AttributeError:
        raise Exception('Out of pages')


def get_animals(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='mw-category')
    animals = [item.text for item in div.find_all('a')]
    if animals is None:
        raise Exception('Invalid tags for get_animals')
    return animals


def get_letter(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    letter = soup.find('div', class_='mw-category').find('h3').text
    if letter is None:
        raise Exception('Invalid tag for get_letter')
    return letter
