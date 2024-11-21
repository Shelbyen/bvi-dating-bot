from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_subject():
    return ['Математика', 'Физика', 'Астрономия', 'Информатика', 'География', 'Экология']


def choosing_sex_kb():
    kb = [[InlineKeyboardButton(text='Мужик', callback_data='0|0|'),
           InlineKeyboardButton(text='Баба', callback_data='0|1|')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def choosing_class_kb():
    kb = [[InlineKeyboardButton(text='9', callback_data='1|9|'),
           InlineKeyboardButton(text='10', callback_data='1|10|'),
           InlineKeyboardButton(text='11', callback_data='1|11|')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def choosing_subject_kb(checked_subject):
    kb = []
    for i in list(zip(*[iter(get_subject())]*3)):

        kb.append([InlineKeyboardButton(text=i[0] + (' ✅' if i[0] in checked_subject else ''), callback_data=f'2|0|' + (i[0] if i[0] not in checked_subject else '-1')),
               InlineKeyboardButton(text=i[1] + (' ✅' if i[1] in checked_subject else ''), callback_data=f'2|0|' + (i[1] if i[1] not in checked_subject else '-1')),
               InlineKeyboardButton(text=i[2] + (' ✅' if i[2] in checked_subject else ''), callback_data=f'2|0|' + (i[2] if i[2] not in checked_subject else '-1'))])
    kb.append([InlineKeyboardButton(text='Готово', callback_data=f'2|1|-1')])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def choosing_priority_kb():
    kb = [[InlineKeyboardButton(text='Парни ✅', callback_data='3|0|'),
           InlineKeyboardButton(text='Девушки ⛔️', callback_data='3|1|')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
