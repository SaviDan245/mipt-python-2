from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.keyboards.abort import get_abort_kb
from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import BUTTONS, TRACK_FREQ_FILEPATH, clean_str

router = Router()


class ChangeFreq(StatesGroup):
    entering_freq = State()


@router.message(F.text == BUTTONS['change_freq'])
async def enter_new_freq(message: Message, state: FSMContext):
    mess = clean_str(LEXICON['enter_new_freq'])
    await message.answer(mess, reply_markup=get_abort_kb())
    await state.set_state(ChangeFreq.entering_freq)


@router.message(ChangeFreq.entering_freq, lambda message: not message.text.isdigit() or
                                                          message.text in list(map(str, range(10))))
async def bad_number(message: Message):
    mess = clean_str(LEXICON['bad_frequency'])
    await message.answer(mess)


@router.message(ChangeFreq.entering_freq, lambda message: message.text.isdigit() and message.text != '0')
async def good_number(message: Message, state: FSMContext):
    with open(TRACK_FREQ_FILEPATH) as f:
        prev_freq = int(f.readline().strip())
    
    new_freq = int(message.text) * 60  # to seconds
    
    with open(TRACK_FREQ_FILEPATH, 'w') as f:
        print(new_freq, file=f)
    
    mess = clean_str(LEXICON['success_change_freq'].format(prev_freq=prev_freq // 60, new_freq=new_freq // 60))
    await message.answer(mess, reply_markup=get_main_kb())  # back to minutes
    await state.clear()
