import logging
from typing import Optional, List

from aiogram import Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from ..handlers.acne_assessment import start_get_anc
from ..handlers.user_registration import start_bot
from ..keyboards.user_menu_kb import user_menu, cancel_send_photo
from ..keyboards.user_registration_kb import choosing_subject_kb
from ..models.subjects import model_to_subject_dict, subjects_dict_to_model, get_subjects_string
from ..schemas.photo_schema import PhotoCreate
from ..schemas.subjects_schema import SubjectsUpdate
from ..schemas.user_schema import UserUpdate, UserBase
from ..services.photo_service import photo_service
from ..services.subjects_service import subjects_service
from ..services.user_service import user_service
from ..use_cases.send_user_info_use_case import generate_all_message

router = Router()


class EditProfile(StatesGroup):
    photo = State()
    subjects = State()


@router.message(or_f(Command(commands=['menu', 'start']), F.text.contains('Моя анкета')))
async def create_menu(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    user = (await state.get_data()).setdefault('user', await user_service.get(str(message.from_user.id)))
    await state.update_data({'user': user})
    if type(message) is not Message:
        message = message.message
    await message.answer('Ваша анкета:\n1 - Изменить фото\n2 - Изменить предметы', reply_markup=user_menu(user.deactivated))
    await generate_all_message(user, message)


@router.message(F.text == 'Заполнить анкету заново')
async def del_me(message: Message, state: FSMContext):
    old_user = (await state.get_data()).setdefault('user', await user_service.get(str(message.from_user.id)))
    await user_service.delete(str(message.from_user.id))
    await message.answer('Удалено.', reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await state.set_data({'old_user': old_user})
    await start_bot(message, state)


@router.message(F.text == 'Смотреть анкеты!')
async def from_menu_to_forms(message: Message, state: FSMContext):
    await start_get_anc(message, state)


@router.message(or_f(F.text.contains('Вкл анкету'), F.text.contains('Выкл анкету')))
async def from_menu_to_forms(message: Message, state: FSMContext):
    user: UserBase = (await state.get_data()).setdefault('user', await user_service.get(str(message.from_user.id)))
    user.deactivated = not user.deactivated
    await user_service.update(user.id, UserUpdate(**user.__dict__))
    if user.deactivated:
        await message.answer('Анкета выключена!', reply_markup=user_menu(user.deactivated))
    else:
        await message.answer('Анкета включена!', reply_markup=user_menu(user.deactivated))


@router.message(F.text.contains('1'))
async def edit_photo(message: Message, state: FSMContext):
    user: UserBase = (await state.get_data()).setdefault('user', await user_service.get(str(message.from_user.id)))
    await state.update_data({'old_photos': user.photos})
    await message.answer('Отправь самое сексуальное фото: ', reply_markup=cancel_send_photo())
    await state.set_state(EditProfile.photo)


@router.message(StateFilter(EditProfile.photo))
async def send_new_photo(message: Message, state: FSMContext, album: Optional[List[Message]] = None):
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
    await photo_service.delete(str(message.from_user.id))
    await photo_service.create_many(media_group)
    await message.answer('Фото обновлено!')
    user: UserBase = (await state.get_data()).setdefault('user', await user_service.get(str(message.from_user.id)))
    await generate_all_message(user, message)

    old_photos = await state.get_value('old_photos')
    edited = {}
    if user.photos != old_photos:
        edited['subjects'] = f"{old_photos} -> {user.photos}"
        logging.info('[Edit profile] ' + str(edited))

    await state.clear()


@router.callback_query(StateFilter(EditProfile.photo), F.data == 'd')
async def delete_photos(call: CallbackQuery, state: FSMContext):
    await photo_service.delete(str(call.from_user.id))
    user = await user_service.get(str(call.from_user.id))
    await state.update_data({'user': user})
    await call.message.delete()
    await generate_all_message(user, call.message)
    await state.clear()


@router.callback_query(StateFilter(EditProfile.photo), F.data == '-')
async def cancel_sending_photo(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()


@router.message(F.text.contains('2'))
async def edit_photo(message: Message, state: FSMContext):
    user: UserBase = (await state.get_data()).setdefault('user', await user_service.get(str(message.from_user.id)))
    send_message = await message.answer('Выберите предметы (можно несколько): ')
    choosing_subject = model_to_subject_dict(user.subjects)
    await state.set_data({'subjects': choosing_subject, 'old_subjects': get_subjects_string(user.subjects)})
    await send_message.edit_reply_markup(reply_markup=choosing_subject_kb(choosing_subject))
    await state.set_state(EditProfile.subjects)


@router.callback_query(StateFilter(EditProfile.subjects), F.data[0] == '2', F.data[2] == '0',
                       F.data[4:6] != '-1')
async def set_subject(call: CallbackQuery, state: FSMContext):
    choosing_subject = (await state.get_data()).setdefault('subjects', {})
    if choosing_subject.get(int(call.data.split('|')[2])):
        choosing_subject.pop(int(call.data.split('|')[2]))
    else:
        choosing_subject[int(call.data.split('|')[2])] = True
    await state.update_data({"subjects": choosing_subject})
    await call.message.edit_reply_markup(reply_markup=choosing_subject_kb(choosing_subject))


@router.callback_query(StateFilter(EditProfile.subjects), F.data[0] == '2', F.data[2] == '1')
async def return_to_menu(call: CallbackQuery, state: FSMContext):
    subjects = (await state.get_data()).setdefault('subjects', {})
    await subjects_service.update(str(call.from_user.id), SubjectsUpdate(**subjects_dict_to_model(subjects)))

    user = await user_service.get(str(call.from_user.id))
    old_subjects = await state.get_value('old_subjects')
    edited = {}
    if get_subjects_string(user.subjects) != old_subjects:
        edited['subjects'] = f"{old_subjects} -> {get_subjects_string(user.subjects)}"
        logging.info('[Edit profile] ' + str(edited))

    await call.message.delete()
    await state.clear()
    await create_menu(call, state)
