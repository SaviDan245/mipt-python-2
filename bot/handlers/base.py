from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import clean_str, BUTTONS

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    mess = clean_str(LEXICON['/start'])
    await message.answer(mess, reply_markup=get_main_kb())


@router.message(F.text == BUTTONS['abort'])
async def abort(message: Message, state: FSMContext):
    mess = clean_str(LEXICON['abort'])
    await message.answer(mess, reply_markup=get_main_kb())
    await state.clear()
