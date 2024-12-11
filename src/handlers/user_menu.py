from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from ..handlers.acne_assessment import start_get_anc
from ..handlers.user_registration import start_bot
from ..keyboards.user_menu_kb import user_menu
from ..services.photo_service import photo_service
from ..services.subjects_service import subjects_service
from ..services.user_service import user_service
from ..use_cases.send_user_info_use_case import generate_all_message

router = Router()


@router.message(or_f(Command(commands=['menu', 'start']), F.text.contains('Моя анкета')))
async def create_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ваша анкета:', reply_markup=user_menu())
    user = (await state.get_data()).setdefault('user', await user_service.get(str(message.from_user.id)))
    await generate_all_message(user, message)


@router.message(F.text == 'Заполнить анкету заново')
async def del_me(message: Message, state: FSMContext):
    old_user = (await state.get_data()).setdefault('user', await user_service.get(str(message.from_user.id)))
    await user_service.delete(str(message.from_user.id))
    await message.answer('Удалено.', reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await state.set_data({'old_user': old_user})
    await start_bot(message, state)


@router.message(F.text == 'Смотреть анкеты!')
async def from_menu_to_forms(message: Message, state: FSMContext):
    await start_get_anc(message, state)
