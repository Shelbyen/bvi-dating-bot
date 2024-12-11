import logging
from typing import Optional, List

from aiogram import F
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from ..keyboards.user_menu_kb import user_menu
from ..keyboards.user_registration_kb import *
from ..models.subjects import subjects_dict_to_model, get_subjects_string
from ..schemas.photo_schema import PhotoCreate
from ..schemas.subjects_schema import SubjectsCreate
from ..schemas.user_schema import UserCreate
from ..services.photo_service import photo_service
from ..services.subjects_service import subjects_service
from ..services.user_service import user_service
from ..use_cases.send_user_info_use_case import generate_all_message

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
    await start_registration(message, state)


async def start_registration(message: Message, state: FSMContext):
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
    await call.message.answer('Напиши свой класс: ', reply_markup=choosing_class_kb())
    await state.set_state(FillingForm.set_class)


@router.message(StateFilter(FillingForm.set_class))
async def set_class(message: Message, state: FSMContext):
    if message.text.isdigit() and len(message.text) < 4:
        if 8 <= int(message.text) <= 11:
            await state.update_data({'school_class': message.text})
            send_message = await message.answer('Выберите предметы (можно несколько): ')
            await send_message.edit_reply_markup(reply_markup=choosing_subject_kb({}))
            await state.set_state(FillingForm.choosing_subjects)
            return
    await message.answer('Введи класс нормально, только число (только с 8 по 11)')


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
    await call.message.answer('Введите ваш город: ', reply_markup=ReplyKeyboardRemove())
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
                media_group.append(PhotoCreate(id=str(message.from_user.id), photo_id=file_id))
            else:
                await message.answer('Это не фото! Отправь нормально! Жду!')
                return
    elif message.photo:
        # await message.bot.download(message.photo[-1], f'photos/{message.from_user.id}_0.jpg')
        media_group.append(PhotoCreate(id=str(message.from_user.id), photo_id=message.photo[-1].file_id))
    else:
        await message.answer('Это не фото! Отправь нормально! Жду!')
        return
    await state.update_data({'photos': media_group})
    await message.answer(
        'Если хочешь добавить в анкету что-то еще, можешь написать сейчас. Например: прошел(-а) все b-side в celeste, мощнейше затащил(-а) всерос, шарю во всех сортах чая и хочу это обсудить и т.п.'
    )
    await state.set_state(FillingForm.write_description)


@router.callback_query(StateFilter(FillingForm.send_photo))
async def set_description(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        'Если хочешь добавить в анкету что-то еще, можешь написать сейчас. Например: прошел(-а) все b-side в celeste, мощнейше затащил(-а) всерос, шарю во всех сортах чая и хочу это обсудить и т.п.'
    )
    await state.set_state(FillingForm.write_description)


@router.message(StateFilter(FillingForm.write_description))
async def set_sex(message: Message, state: FSMContext):
    person = await state.get_data()
    person['description'] = message.text
    subjects = person.setdefault('subjects', {})
    photos = person.setdefault('photos', [])
    old_user = person.get('old_user')

    # person.pop('subjects')
    subjects = SubjectsCreate(id=str(message.from_user.id), **subjects_dict_to_model(subjects))
    user = UserCreate(id=str(message.from_user.id), **person)

    # person.update({'subjects': SubjectsCreate(id=str(message.from_user.id), **subjects_dict_to_model(subjects))})
    await user_service.create(user)
    await subjects_service.create(subjects)
    await photo_service.create_many(photos)

    await message.answer('Поздравляю с успешной регистрацией!!!', reply_markup=user_menu(False))
    user = await user_service.get(user.id)
    await generate_all_message(user, message)

    if old_user:
        old_user = old_user.__dict__
        old_user.pop('_sa_instance_state')
        old_user.pop('updated_at')
        old_user.pop('created_at')
        old_user.pop('id')
        edited = {}
        person.pop('old_user')
        person.pop('subjects')
        person['sex'] = bool(person['sex'])
        person['priority'] = bool(person['priority']) if person['priority'] else None
        for i in person:
            if str(person[i]) != str(old_user[i]):
                edited[i] = f"{old_user[i]} -> {person[i]}"
        if get_subjects_string(user.subjects) != get_subjects_string(old_user['subjects']):
            edited['subjects'] = f"{get_subjects_string(old_user['subjects'])} -> {get_subjects_string(user.subjects)}"
        if len(edited) > 0:
            logging.info('[Edit profile] ' + str(edited))
    else:
        logging.info('[New profile] ' + str(message.from_user.id))

    await state.clear()
