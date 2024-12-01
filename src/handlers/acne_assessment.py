from typing import Optional

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InputMediaPhoto

from ..keyboards.user_kb import *
from ..models.subjects import get_subjects_string
from ..services.photo_service import photo_service
from ..services.subjects_service import subjects_service
from ..services.user_service import user_service

router = Router()


class ViewForm(StatesGroup):
    view_form = State()
    set_reaction = State()


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


def print_user(user_model, subjects, photos_exist):
    t = ''
    if not photos_exist:
        t += 'Нет фотографий!\n'
    t = 'Имя: ' + user_model.name + '\n'
    t += 'Пол: ' + digit_to_sex(user_model.sex) + '\n'
    t += 'Кем интересуется: ' + digit_to_sex(user_model.priority, True) + '\n'
    t += 'Город: ' + user_model.town + '\n'
    t += 'Класс: ' + str(user_model.school_class) + '\n'
    t += 'Предметы: ' + get_subjects_string(subjects) + '\n'
    t += 'Описание: ' + user_model.description
    return t


def generate_media_group(photos, message_text):
    media_group = []
    for msg in photos:
        media_group.append(InputMediaPhoto(media=msg.photo_id))
    if len(media_group) > 0:
        media_group[0].caption = message_text
    return media_group


async def generate_all_message(user, message):
    message_text = print_user(user, user.subjects, len(user.photos) != 0)
    if len(user.photos) > 0:
        await message.answer_media_group(generate_media_group(user.photos, message_text))
        return
    await message.answer(message_text)


@router.message(Command('get_anc'), StateFilter(None))
async def start_get_anc(message: Message, state: FSMContext):
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
    # if bot_answer:
    #     await message.answer(bot_answer)
    # else:
    #     await message.answer('Признание в любви успешно отправлено!!!')
    await get_anc(message, state)


@router.message(F.text == '👎', StateFilter(ViewForm.view_form))
async def skip_negative(message: Message, state: FSMContext):
    form_user_id = await state.get_value('id')
    bot_answer = await send_message_to_another(message.bot, 'Тебя невзлюбил @' + str(message.from_user.username),
                                               form_user_id)
    # if bot_answer:
    #     await call.answer(bot_answer)
    # else:
    #     await call.answer('Признание в ненависти успешно отправлено!!!')
    await get_anc(message, state)


@router.message(F.text == 'Скип', StateFilter(ViewForm.view_form))
async def skip_anc(message: Message, state: FSMContext):
    await get_anc(message, state)


@router.message(StateFilter(None))
async def start_anc_past_reload(message: Message, state: FSMContext):
    await start_get_anc(message, state)


@router.message(Command('get_me'), StateFilter(None))
async def get_me(message: Message, state: FSMContext):
    print(1)
    random_user = await user_service.get(str(message.from_user.id))
    await generate_all_message(random_user, message)
    await state.clear()


@router.message(Command('del_me'))
async def del_me(message: Message, state: FSMContext):
    await subjects_service.delete(str(message.from_user.id))
    await photo_service.delete(str(message.from_user.id))
    await user_service.delete(str(message.from_user.id))
    await message.answer('Удалено.')
    await state.clear()
