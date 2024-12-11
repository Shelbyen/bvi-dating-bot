from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from ..keyboards.user_kb import *
from ..services.user_service import user_service
from ..use_cases.send_user_info_use_case import generate_all_message, send_message_to_another

router = Router()


class ViewForm(StatesGroup):
    view_form = State()
    set_reaction = State()


@router.message(Command(commands=['get_anc']))
async def start_get_anc(message: Message, state: FSMContext):
    if (await state.get_state()) != ViewForm.view_form:
        await message.answer('Давай посмотрим кого я могу тебе предложить...', reply_markup=choosing_reaction())
    await state.set_state(ViewForm.view_form)
    await get_anc(message, state)


async def get_anc(message: Message, state: FSMContext):
    random_user = await user_service.get_random_user()
    await state.update_data({'id': int(random_user.id)})
    await generate_all_message(random_user, message)


@router.message(F.text == '❤️', StateFilter(ViewForm.view_form))
async def send_love(message: Message, state: FSMContext):
    form_user_id = await state.get_value('id')
    bot_answer = await send_message_to_another(message.bot, 'Тебя полюбил @' + str(message.from_user.username),
                                               form_user_id)
    await get_anc(message, state)


@router.message(F.text == '👎', StateFilter(ViewForm.view_form))
async def skip_negative(message: Message, state: FSMContext):
    form_user_id = await state.get_value('id')
    bot_answer = await send_message_to_another(message.bot, 'Тебя невзлюбил @' + str(message.from_user.username),
                                               form_user_id)
    await get_anc(message, state)


@router.message(F.text == 'Скип', StateFilter(ViewForm.view_form))
async def skip_anc(message: Message, state: FSMContext):
    await get_anc(message, state)
