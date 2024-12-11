from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InputMediaPhoto

from src.models.subjects import get_subjects_string


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
