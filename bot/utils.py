import os
import random
from typing import List

import pandas as pd

LINKS_FILEPATH = os.path.join('dbs', 'links.csv')
REALTY_FILEPATH = os.path.join('dbs', 'realty.db')
TRACK_FREQ_FILEPATH = os.path.join('dbs', 'track_freq.txt')
FILES_FILEPATH = os.path.join('bot', 'files')
XLSX_FILEPATH = os.path.join('bot', 'files', 'realty_database.xlsx')

N_TILDAS = 30
ADD_RANDOM_MINUTES = list(range(-5, 6))

REALTY_COLUMNS = [
    'Название',
    'Ссылка на объявление',
    'ID объявления',
    'Дата публикации',
    'Цена',
    'Адрес',
    'Площадь помещения',
    'Количество комнат',
    'Этаж помещения',
    'Макс. этаж здания',
    'Ссылка на Google-карты'
]

BUTTONS = {
    'list_links': '🧾 Список отслеживаемых ссылок',
    'send_offers': '🔗 Вывести новые офферы по ссылкам',
    'add_link': '➕ Отслеживать новую ссылку',
    'remove_link': '🚫 Удалить ссылку из отслеживаемых',
    'send_realty_db': '💽 Скачать базу данных',
    'change_freq': '🔢 Изменить частоту уведомлений',
    'abort': '❌ Отмена',
    'begin_tracking': '✅ Начать отслеживание',
    'stop_tracking': '⛔ Приостановить отслеживание',
}


def clean_str(string: str) -> str:
    return string.replace('.', r'\.')\
        .replace('-', r'\-')\
        .replace('!', r'\!')\
        .replace('<', r'\<')\
        .replace('>', r'\>')


def check_link(link: str) -> str:
    if link.startswith('http'):  # and requests.get(link).status_code == 200:
        data = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)
        if link in data['url'].values:
            return 'existing link'
        return 'good link'
    return 'bad link'


def beautify_price(price: int) -> str:
    string = ''
    for i, c in enumerate(str(price)[::-1]):
        string += c
        if i % 3 == 2:
            string += ' '
    return '₽ ' + string[::-1]


def parse_offers(offers: List[dict]) -> List[str]:
    messages = []
    for offer in offers:
        text = ''
        text += f'[*Ссылка на объявление*]({offer["url"]})\n'
        text += f'*Название:* {offer["title"]}\n'
        text += f'*Адрес:* [{offer["adress"]}]({offer["location_link"]})\n'
        text += f'*Стоимость:* {beautify_price(offer["price"])}\n'
        text += f'*Всего комнат в квартире:* {offer["rooms"]}\n'
        text += f'*Площадь помещения:* {offer["area"]} кв. м.\n'
        text += f'*Этаж помещения/этаж дома:* {offer["floor"]}/{offer["total_floor"]}\n'
        text += f'*Дата публикации:* {offer["date"]}\n'
        text += r'\~' * N_TILDAS + '\n'
        messages.append(text)
    return messages


def update_links(sample: dict) -> None:
    data = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)
    new_link = pd.DataFrame({'header': [sample['header']], 'url': [sample['url']]})
    upd_data = pd.concat([data, new_link])
    upd_data.to_csv(LINKS_FILEPATH)


def get_freq() -> int:
    with open(TRACK_FREQ_FILEPATH) as f:
        freq = int(f.readline())  # in seconds
    
    return freq + random.choice(ADD_RANDOM_MINUTES) * 60


if __name__ == '__main__':
    print(check_link(''))
