from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.models.subjects import Subjects


def choosing_sex_kb():
    kb = [[InlineKeyboardButton(text='Парень', callback_data='0|0|'),
           InlineKeyboardButton(text='Девушка', callback_data='0|1|')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def choosing_class_kb():
    kb = [[InlineKeyboardButton(text='9', callback_data='1|9|'),
           InlineKeyboardButton(text='10', callback_data='1|10|'),
           InlineKeyboardButton(text='11', callback_data='1|11|')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def choosing_subject_kb(checked_subject):
    kb = []
    for i in list(zip(*[iter(Subjects)]*3)):
        t = []
        for j in i:
            t.append(InlineKeyboardButton(text=j.get_localized_name() + (' ✅' if i[0] in checked_subject else ''),
                                          callback_data=f'2|0|' + (j.value if j.value not in checked_subject else '-1')))
        kb.append(t)
    kb.append([InlineKeyboardButton(text='Готово', callback_data=f'2|1|-1')])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def choosing_priority_kb():
    kb = [[InlineKeyboardButton(text='Парни ✅', callback_data='3|0|'),
           InlineKeyboardButton(text='Девушки ⛔️', callback_data='3|1|')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def choosing_reaction(pk):
    kb = [[InlineKeyboardButton(text='❤️', callback_data=f'4|0|{pk}'),
           InlineKeyboardButton(text='👎', callback_data=f'4|1|{pk}')],
          [InlineKeyboardButton(text='Скип', callback_data=f'4|2|{pk}')]]
    return InlineKeyboardMarkup(inline_keyboard=kb, one_time_keyboard=True)
