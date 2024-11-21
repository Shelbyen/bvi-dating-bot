from typing import Callable, Dict, Any, Awaitable

from aiogram.types import TelegramObject, Message, CallbackQuery

from src.services.user_service import user_service


class PermissionMiddleware:
    def __init__(self, is_exists=True):
        self.is_exists = is_exists

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user = await user_service.exists(str(event.from_user.id))
        if user == self.is_exists:
            return await handler(event, data)
        return None
