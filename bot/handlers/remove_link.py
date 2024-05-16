import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.keyboards.abort import get_abort_kb
from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import LINKS_FILEPATH, clean_str, BUTTONS

router = Router()


class RemoveLink(StatesGroup):
    checking_number = State()


@router.message(F.text == BUTTONS['remove_link'])
async def paste_new_link(message: Message, state: FSMContext):
    data = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)
    if len(data) == 0:
        mess = clean_str(LEXICON['empty_links'])
        await message.answer(mess, reply_markup=get_main_kb())
    else:
        text = LEXICON['list_entry']
        for i, [header, url] in enumerate(zip(data['header'], data['url'])):
            text += f'{i + 1}. [{header}]({url})\n'
        await message.answer(clean_str(text), reply_markup=get_abort_kb())
        mess = clean_str(LEXICON['number_remove_link'])
        await message.answer(mess)
        await state.set_state(RemoveLink.checking_number)


@router.message(RemoveLink.checking_number, lambda message: not message.text.isdigit() or message.text == '0')
async def bad_number(message: Message):
    mess = clean_str(LEXICON['bad_number'])
    await message.answer(mess)


@router.message(RemoveLink.checking_number, lambda message: message.text.isdigit() and message.text != '0')
async def good_number(message: Message, state: FSMContext):
    idx = int(message.text) - 1
    goal_header = ''
    data = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)

    for i, header in enumerate(data['header']):
        if i == idx:
            goal_header = header
            break

    if not goal_header:
        mess = clean_str(LEXICON['not_existing_number'])
        await message.answer(mess)
    else:
        upd_data = data[data['header'] != goal_header]
        upd_data.to_csv(LINKS_FILEPATH)

        mess = clean_str(LEXICON['success_remove_link'])
        await message.answer(mess, reply_markup=get_main_kb())
        await state.clear()
