from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.keyboards.abort import get_abort_kb
from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import check_link, clean_str, update_links, BUTTONS

router = Router()


class NewLink(StatesGroup):
    pasting_new_link = State()
    heading = State()


@router.message(F.text == BUTTONS['add_link'])
async def paste_new_link(message: Message, state: FSMContext):
    mess = clean_str(LEXICON['paste_new_link'])
    await message.answer(mess, reply_markup=get_abort_kb())
    await state.set_state(NewLink.pasting_new_link)


@router.message(NewLink.pasting_new_link, lambda message: check_link(message.text) == 'bad link')
async def new_link_is_bad(message: Message):
    mess = clean_str(LEXICON['error_paste_new_link'])
    await message.answer(mess)


@router.message(NewLink.pasting_new_link, lambda message: check_link(message.text) == 'existing link')
async def new_link_is_bad(message: Message):
    mess = clean_str(LEXICON['existing_link'])
    await message.answer(mess, reply_markup=get_main_kb())


@router.message(NewLink.pasting_new_link, lambda message: check_link(message.text) == 'good link')
async def new_link_is_good(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    mess = clean_str(LEXICON['paste_new_heading'])
    await message.answer(mess)
    await state.set_state(NewLink.heading)


@router.message(NewLink.heading)
async def paste_new_heading(message: Message, state: FSMContext):
    await state.update_data(header=message.text)
    sample = await state.get_data()
    update_links(sample)
    await state.clear()

    mess = clean_str(LEXICON['success_new_link'])
    await message.answer(mess, reply_markup=get_main_kb())
