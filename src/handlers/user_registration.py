from typing import Optional, List

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import F

from ..keyboards.user_kb import *
from ..models.subjects import subjects_dict_to_model
from ..schemas.subjects_schema import SubjectsCreate
from ..schemas.user_schema import UserCreate
from ..services.subjects_service import subjects_service
from ..services.user_service import user_service

router = Router()


class FillingForm(StatesGroup):
    write_name = State()
    set_sex = State()
    set_class = State()
    choosing_subjects = State()
    write_town = State()
    set_priority = State()
    send_photo = State()
    write_description = State()


@router.message(Command('start'), StateFilter(None))
async def start_bot(message: Message, state: FSMContext):
    if await state.get_state() is not None:
        return
    await message.answer('@Test123321hahaBot\n/start - зарегаться\n/get_anc - случайная анкета\n/del_me - удалить себя')
    await message.answer('Имя: ', parse_mode="Markdown")
    await state.set_state(FillingForm.write_name)


@router.message(StateFilter(FillingForm.write_name))
async def write_name(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer('Выберите пол: ', reply_markup=choosing_sex_kb())
    await state.set_state(FillingForm.set_sex)


@router.callback_query(StateFilter(FillingForm.set_sex), F.data[0] == '0')
async def set_sex(call: CallbackQuery, state: FSMContext):
    await state.update_data({'sex': call.data.split('|')[1]})
    await call.message.answer('Выберите класс обучения: ', reply_markup=choosing_class_kb())
    await state.set_state(FillingForm.set_class)


@router.callback_query(StateFilter(FillingForm.set_class), F.data[0] == '1')
async def set_class(call: CallbackQuery, state: FSMContext):
    await state.update_data({'school_class': call.data.split('|')[1]})
    await call.message.answer('Выберите предметы (можно несколько): ', reply_markup=choosing_subject_kb([]))
    await state.set_state(FillingForm.choosing_subjects)


@router.callback_query(StateFilter(FillingForm.choosing_subjects), F.data[0] == '2', F.data[2] == '0',
                       F.data[4:6] != '-1')
async def set_subject(call: CallbackQuery, state: FSMContext):
    choosing_subject = (await state.get_data()).setdefault('subjects', {})
    if choosing_subject.get(int(call.data.split('|')[2])):
        choosing_subject.pop(int(call.data.split('|')[2]))
    else:
        choosing_subject[int(call.data.split('|')[2])] = True
    await state.update_data({"subjects": choosing_subject})
    await call.message.edit_reply_markup(reply_markup=choosing_subject_kb(choosing_subject))


@router.callback_query(StateFilter(FillingForm.choosing_subjects), F.data[0] == '2', F.data[2] == '1')
async def set_town(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите ваш город: ')
    await state.set_state(FillingForm.write_town)


@router.message(StateFilter(FillingForm.write_town))
async def set_priority(message: Message, state: FSMContext):
    await state.update_data({'town': message.text})
    await message.answer('Выберите кто интересует: ', reply_markup=choosing_priority_kb())
    await state.set_state(FillingForm.set_priority)


@router.callback_query(StateFilter(FillingForm.set_priority), F.data[0] == '3')
async def send_photo(call: CallbackQuery, state: FSMContext):
    await state.update_data({'priority': None if call.data.split('|')[1] == '2' else call.data.split('|')[1]})
    await call.message.answer('Отправь самое сексуальное фото: ', reply_markup=skip_send_photo())
    await state.set_state(FillingForm.send_photo)


@router.message(StateFilter(FillingForm.send_photo))
async def set_description_with_photo(message: Message, state: FSMContext, album: Optional[List[Message]] = None):
    media_group = []
    if album:
        for i, msg in enumerate(album):
            if msg.photo:
                file_id = msg.photo[-1].file_id
                await message.bot.download(msg.photo[-1], f'{message.from_user.id}_{i}')
                media_group.append(InputMediaPhoto(media=file_id, caption=msg.caption))
            else:
                await message.answer('Это не фото! Отправь нормально! Жду!')
                return
        await state.update_data({'photo_count': len(album)})
    elif message.photo:
        await message.bot.download(message.photo[-1], f'photos/{message.from_user.id}_0.jpg')
        await state.update_data({'photo_count': 1})
    else:
        await message.answer('Это не фото! Отправь нормально! Жду!')
        return

    await message.answer(
        'Если хочешь добавить в анкету что-то еще, можешь написать сейчас. Например: прошел(-а) все b-side в celeste, мощнейше затащил(-а) всерос, шарю во всех сортах чая и хочу это обсудить и т.п.'
    )
    await state.set_state(FillingForm.write_description)

@router.callback_query(StateFilter(FillingForm.send_photo))
async def set_description(call: CallbackQuery, state: FSMContext):
    await state.update_data({'photo_count': 0})
    await call.message.answer(
        'Если хочешь добавить в анкету что-то еще, можешь написать сейчас. Например: прошел(-а) все b-side в celeste, мощнейше затащил(-а) всерос, шарю во всех сортах чая и хочу это обсудить и т.п.'
    )
    await state.set_state(FillingForm.write_description)


@router.message(StateFilter(FillingForm.write_description))
async def set_sex(message: Message, state: FSMContext):
    person = await state.get_data()
    person['description'] = message.text
    subjects = person.setdefault('subjects', {})
    person.pop('subjects')
    person.pop('photo_count')
    await user_service.create(UserCreate(id=str(message.from_user.id), **person))
    await subjects_service.create(SubjectsCreate(id=str(message.from_user.id), **subjects_dict_to_model(subjects)))
    await message.answer('Поздравляю с успешной регистрацией!!!')
    print('Новый пользователь: ' + str(message.from_user.username))
    await state.clear()
