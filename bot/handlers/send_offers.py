import pandas as pd
from aiogram import Router, F
from aiogram.types import Message
from selenium import webdriver

from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import clean_str, LINKS_FILEPATH, parse_offers, BUTTONS, N_TILDAS
from parsers.avito import get_new_offers_by_driver

router = Router()


@router.message(F.text == BUTTONS['send_offers'])
async def send_new_offers(message: Message):
    data = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)
    if len(data) == 0:
        mess = clean_str(LEXICON['empty_links'])
        await message.answer(mess, reply_markup=get_main_kb())
    else:
        driver = webdriver.Firefox()

        for i, [header, url] in enumerate(zip(data['header'], data['url'])):
            driver.get(url)

            raw_offers = get_new_offers_by_driver(driver, message.from_user.id)
            new_offers = parse_offers(raw_offers)
            if not new_offers:
                continue
            # header_mess = clean_str(f'*Ссылка №{i + 1}. [{header}]({url})*\n\n' + r'\~' * N_TILDAS + '\n\n')
            # await message.answer(header_mess)
            for text in new_offers:
                htext = f'__*От ссылки: {header}*__\n\n' + r'\~' * N_TILDAS + '\n\n' + text
                mess = clean_str(htext)
                await message.answer(mess)

        driver.quit()
