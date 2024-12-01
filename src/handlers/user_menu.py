from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(Command(commands=['menu', 'start']))
async def create_menu(message: Message, state: FSMContext):
    await message.answer('Вот ваше меню, господин')
