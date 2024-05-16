import pandas as pd
from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import LINKS_FILEPATH, clean_str, BUTTONS

router = Router()


@router.message(F.text == BUTTONS['list_links'])
async def show_links(message: Message):
    data = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)
    if len(data) == 0:
        mess = clean_str(LEXICON['empty_links'])
        await message.answer(mess, reply_markup=get_main_kb())
    else:
        text = LEXICON['list_entry']
        for i, [header, url] in enumerate(zip(data['header'], data['url'])):
            text += f'{i + 1}. [{header}]({url})\n'
        await message.answer(clean_str(text), reply_markup=get_main_kb())
