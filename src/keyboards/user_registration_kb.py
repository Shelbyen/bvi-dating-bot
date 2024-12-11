from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from src.models.subjects import Subjects


def choosing_sex_kb():
    kb = [[InlineKeyboardButton(text='Парень', callback_data='0|0|'),
           InlineKeyboardButton(text='Девушка', callback_data='0|1|')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def choosing_class_kb():
    kb = [[KeyboardButton(text='9'),
           KeyboardButton(text='10'),
           KeyboardButton(text='11')]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder='Напиши свой класс')


def choosing_subject_kb(checked_subject):
    kb = []
    for i in list(zip(*[iter(Subjects)] * 3)):
        t = []
        for j in i:
            t.append(InlineKeyboardButton(text=j.get_localized_name() + (' ✅' if j.value in checked_subject else ''),
                                          callback_data=f'2|0|' + str(j.value)))
        kb.append(t)
    kb.append([InlineKeyboardButton(text='Готово', callback_data=f'2|1|-1')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def choosing_priority_kb():
    kb = [[InlineKeyboardButton(text='Парни ✅', callback_data='3|0|'),
           InlineKeyboardButton(text='Девушки ⛔️', callback_data='3|1|')],
          [InlineKeyboardButton(text='ВСЕ!', callback_data='3|2|')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def skip_send_photo():
    kb = [[InlineKeyboardButton(text='Скип', callback_data='-')]]
    return InlineKeyboardMarkup(inline_keyboard=kb, one_time_keyboard=True)
