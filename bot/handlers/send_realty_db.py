import os

import pandas as pd
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from selenium import webdriver

from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import clean_str, BUTTONS, REALTY_COLUMNS, LINKS_FILEPATH, XLSX_FILEPATH, FILES_FILEPATH
from parsers.avito import get_new_offers_by_driver

router = Router()


@router.message(F.text == BUTTONS['send_realty_db'])
async def send_realty_db(message: Message):
    links = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)

    if len(links) != 1:
        mess = clean_str(LEXICON['not_one_link'])
        await message.answer(mess, reply_markup=get_main_kb())
    else:
        mess = clean_str(LEXICON['loading_realty'])
        await message.answer(mess)

        url: str = links['url'][0]
        export_df = pd.DataFrame(columns=REALTY_COLUMNS)
        
        driver = webdriver.Firefox()

        for page in range(1, 101):
            print(f'Read page #{page}')

            driver.get(url + f'&p={page}')
            raw_offers = get_new_offers_by_driver(driver, message.from_user.id, update_db=False)
            if not raw_offers:
                driver.quit()
                break
            values_list = [list(d.values())[:-1] for d in raw_offers]
            export_df = pd.concat([export_df, pd.DataFrame(values_list, columns=REALTY_COLUMNS)])
        
        if not os.path.exists(FILES_FILEPATH):
            os.mkdir(FILES_FILEPATH)
        
        export_df.to_excel(XLSX_FILEPATH)

        file = FSInputFile(XLSX_FILEPATH)
        await message.answer_document(file)
