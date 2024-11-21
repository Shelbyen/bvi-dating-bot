from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..services.subjects_service import subjects_service
from ..services.user_service import user_service
from ..keyboards.user_kb import *

router = Router()

def print_user(user_model, subjects):
    t = 'Имя: ' + user_model.name + '\n'
    t += 'Город: ' + user_model.town + '\n'
    t += 'Класс: ' + str(user_model.school_class) + '\n'
    t += 'Предметы: ' + get_subject_string(subjects) + '\n'
    t += 'Описание: ' + user_model.description
    return t


@router.message(Command('get_anc'))
async def get_anc(message: Message):
    random_user = await user_service.get_random_user()
    user_subjects = await subjects_service.get(random_user.id)
    print(print_user(random_user, user_subjects))
    await message.answer(print_user(random_user, user_subjects))

@router.message(Command('del_me'))
async def get_anc(message: Message):
    await subjects_service.delete(str(message.from_user.id))
    await user_service.delete(str(message.from_user.id))
    await message.answer('Удалено.')
