from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from ..models.user_model import UserModel


def user_menu(user: UserModel):
    kb = [
        [KeyboardButton(text='Включить анкету!' if user.deactivated else 'Выключить анкету!')],
        [KeyboardButton(text='Заполнить анкету заново')],
        [KeyboardButton(text='Смотреть анкеты!')]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
