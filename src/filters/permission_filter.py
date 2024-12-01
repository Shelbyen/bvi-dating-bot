from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.services.user_service import user_service


class PermissionFilter(BaseFilter):
    def __init__(self, is_exists: bool = True) -> None:
        self.is_exists = is_exists

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = await user_service.exists(str(event.from_user.id))
        return user == self.is_exists
