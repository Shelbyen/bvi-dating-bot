from typing import Any

from aiogram.filters import Filter
from aiogram.types import Message

from src.services.user_service import user_service


class ExistsFilter(Filter):
    async def __call__(self, message: Message) -> bool | dict[str, Any]:
        return await user_service.exists(str(message.from_user.id))