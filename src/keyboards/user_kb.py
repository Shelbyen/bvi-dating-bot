from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def choosing_reaction():
    kb = [[KeyboardButton(text='❤️'),
           KeyboardButton(text='👎')],
          [KeyboardButton(text='Скип')],
          [KeyboardButton(text='Моя анкета')]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
