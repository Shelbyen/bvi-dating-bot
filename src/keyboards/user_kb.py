from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_subject():
    return {'math': 'Математика', 'physics': 'Физика', 'astronomy': 'Астрономия', 'computer_science': 'Информатика', 'geography': 'География', 'ecology': 'Экология'}
def get_subject_string(subs):
    subjects = get_subject()
    subs = {k: v for k, v in subs.__dict__.items() if subjects.get(k)}
    return ', '.join(subjects[i] for i in subs if subs[i])


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
    subs = get_subject()
    for i in list(zip(*[iter(subs)]*3)):
        kb.append([InlineKeyboardButton(text=subs[i[0]] + (' ✅' if i[0] in checked_subject else ''), callback_data=f'2|0|' + (i[0] if i[0] not in checked_subject else '-1')),
               InlineKeyboardButton(text=subs[i[1]] + (' ✅' if i[1] in checked_subject else ''), callback_data=f'2|0|' + (i[1] if i[1] not in checked_subject else '-1')),
               InlineKeyboardButton(text=subs[i[2]] + (' ✅' if i[2] in checked_subject else ''), callback_data=f'2|0|' + (i[2] if i[2] not in checked_subject else '-1'))])
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
