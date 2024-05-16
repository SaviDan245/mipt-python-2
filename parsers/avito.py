import json
from datetime import datetime
from typing import Union, List
from urllib.parse import unquote

from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from dbs.fetch_db import update_database

SITE = 'https://www.avito.ru'


def get_json(driver: WebDriver) -> dict:
    """
    Получить JSON-словарь из HTML-кода страницы
    :param url: адрес поисковой строки с фильтрами и сортировкой по дате
    :return: JSON-словарь
    """

    html = driver.execute_script("return document.documentElement.outerHTML;")
    if 'Ничего не найдено' in html:
        return {}

    tree = HTMLParser(html)
    scripts = tree.css('script')

    json_data: dict = {}

    for script in scripts:
        if 'window.__initialData__' in script.text():
            # print('HERE')
            json_raw = unquote(script.text().split(';')[0].split('=')[1].strip().strip('"'))
            json_data = json.loads(json_raw)

    return json_data


def get_offer(item: dict, user_id: int) -> Union[None, dict]:
    """
    Распарсить оффер для добавления в базу данных
    :param item: JSON оффера
    :return: необходимые данные из оффера (в случае успеха)
    """
    try:
        timestamp = datetime.fromtimestamp(item['sortTimeStamp'] / 1000)

        if len(item['geo']['geoReferences']):
            city = item['geo']['geoReferences'][0]['content']
        else:
            city = '?'
        adress = item['geo']['formattedAddress']
        coords = f'{item["coords"]["lat"]},{item["coords"]["lng"]}'

        raw_title = item['title'].split(', ')
        area = float(raw_title[0].split()[1].replace(',', '.'))
        rooms = raw_title[0].split()[-1][0]
        floor, total_floor = map(int, raw_title[1].split()[0].split('/'))

        offer = {
            'title': item['title'].replace('\xa0', ' '),
            'url': SITE + item['urlPath'],
            'offer_id': item['id'],
            'date': datetime.strftime(timestamp, '%d.%m.%Y в %H:%M'),
            'price': item['priceDetailed']['value'],
            'adress': city + ', ' + adress,
            'area': area,
            'rooms': rooms,
            'floor': floor,
            'total_floor': total_floor,
            'location_link': 'https://www.google.com/maps/search/?api=1&query=' + coords,
            'user_id': user_id
        }

    except Exception as e:
        print(item)
        print(e)
        exit(0)
    else:
        return offer


def upload_offers(data: dict, user_id: int, update_db: bool) -> List[dict]:
    """
    Обновить базу данных новыми офферами
    :param data: JSON-словарь
    :return: список объявлений с необходимыми данными
    """
    # print(data)
    target_key = None
    for key in data.keys():
        if 'single-page' in key:
            target_key = key
            break

    if target_key is None:
        raise (KeyError('Искомый ключ не найден в JSON'))

    new_offers: List[dict] = []

    for item in data[target_key]['data']['catalog']['items']:
        if item.get('id'):
            offer: dict = get_offer(item, user_id)
            if offer:
                if not update_db:
                    new_offers.append(offer)
                    continue
                response: bool = update_database(offer)
                if response:
                    new_offers.append(offer)
                    print(f'Оффер {item["id"]} добавлен в базу данных')
                else:
                    print(f'Оффер {item["id"]} уже добавлен в базу данных.')
            else:
                print(f'Не удалось добавить оффер {item["id"]} в базу данных.')

    return new_offers


def get_new_offers_by_driver(driver: WebDriver, user_id: int, update_db: bool = True) -> list:
    json_data = get_json(driver)

    if not json_data:
        return []

    result = upload_offers(json_data, user_id, update_db)
    return result


def get_new_offers(url: str, user_id: int, update_db: bool = True) -> list:
    driver = webdriver.Firefox()
    driver.get(url)

    print('Got URL')

    json_data = get_json(driver)

    print('Got JSON')

    # driver.quit()
    if not json_data:
        return []

    result = upload_offers(json_data, user_id, update_db)

    print('Got results')

    return result


if __name__ == '__main__':
    new_offers = get_new_offers('https://www.avito.ru/kazan/komnaty/prodam-ASgBAgICAUSQA7wQ?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&f=ASgBAgECAUSQA7wQAkX6BxV7ImZyb20iOjE2LCJ0byI6bnVsbH3GmgwXeyJmcm9tIjowLCJ0byI6MjAwMDAwMH0&s=104')
    print(new_offers)
