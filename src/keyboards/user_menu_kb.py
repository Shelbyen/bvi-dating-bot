from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def user_menu():
    kb = [[KeyboardButton(text='Заполнить анкету заново')], [KeyboardButton(text='Смотреть анкеты!')]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
