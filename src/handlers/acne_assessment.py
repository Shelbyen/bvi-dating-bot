from typing import Optional

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from ..keyboards.user_kb import *
from ..models.subjects import get_subjects_string
from ..services.subjects_service import subjects_service
from ..services.user_service import user_service

router = Router()


def digit_to_sex(d, p_mode=False):
    if d is None:
        return 'Все!'
    if not p_mode:
        return 'Девушка' if d else 'Парень'
    return 'Девушки' if d else 'Парни'


async def send_message_to_another(bot: Bot, message: str, to_user: str) -> Optional[str]:
    try:
        await bot.send_message(to_user, message)
    except TelegramForbiddenError:
        return 'Пользователь забанил бота'
    else:
        return None


def print_user(user_model, subjects):
    t = 'Имя: ' + user_model.name + '\n'
    t += 'Пол: ' + digit_to_sex(user_model.sex) + '\n'
    t += 'Кем интересуется: ' + digit_to_sex(user_model.priority, True) + '\n'
    t += 'Город: ' + user_model.town + '\n'
    t += 'Класс: ' + str(user_model.school_class) + '\n'
    t += 'Предметы: ' + get_subjects_string(subjects) + '\n'
    t += 'Описание: ' + user_model.description
    return t


@router.message(Command('get_anc'))
async def get_anc(message: Message):
    random_user = await user_service.get_random_user()
    user_subjects = await subjects_service.get(random_user.id)
    print(print_user(random_user, user_subjects))
    await message.answer(print_user(random_user, user_subjects), reply_markup=choosing_reaction(random_user.id))


@router.callback_query(F.data[0] == '4', F.data[2] == '0')
async def send_love(call: CallbackQuery):
    bot_answer = await send_message_to_another(call.bot, 'Тебя полюбил @' + str(call.from_user.username),
                                               call.data.split('|')[2])
    if bot_answer:
        await call.answer(bot_answer)
    else:
        await call.answer('Признание в любви успешно отправлено!!!')
    await get_anc(call.message)


@router.callback_query(F.data[0] == '4', F.data[2] == '1')
async def skip_negative(call: CallbackQuery):
    bot_answer = await send_message_to_another(call.bot, 'Тебя невзлюбил @' + str(call.from_user.username),
                                               call.data.split('|')[2])
    if bot_answer:
        await call.answer(bot_answer)
    else:
        await call.answer('Признание в ненависти успешно отправлено!!!')
    await get_anc(call.message)


@router.callback_query(F.data[0] == '4', F.data[2] == '2')
async def skip_anc(call: CallbackQuery):
    await get_anc(call.message)


@router.message(Command('del_me'))
async def del_me(message: Message):
    await subjects_service.delete(str(message.from_user.id))
    await user_service.delete(str(message.from_user.id))
    await message.answer('Удалено.')
