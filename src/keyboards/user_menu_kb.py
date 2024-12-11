from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def user_menu(deactivated: bool):
    kb = [
        [KeyboardButton(text='1'),
         KeyboardButton(text='2'),
         KeyboardButton(text='Вкл анкету' if deactivated else 'Выкл анкету')],
        [KeyboardButton(text='Заполнить анкету заново')],
        [KeyboardButton(text='Смотреть анкеты!')]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def cancel_send_photo():
    kb = [[InlineKeyboardButton(text='Удалить все', callback_data='d')],
          [InlineKeyboardButton(text='Оставить как есть', callback_data='-')]]
    return InlineKeyboardMarkup(inline_keyboard=kb, one_time_keyboard=True)