from typing import Optional

from src.services.base_service import BaseService
from ..repositories.sqlalchemy_repository import ModelType
from ..repositories.user_repository import user_repository


class UserService(BaseService):
    async def exists(self, user_id: str) -> bool:
        return await self.repository.exists(id=user_id)

    async def get_random_user(self) -> Optional[ModelType] | None:
        return await self.repository.get_random()


user_service = UserService(repository=user_repository)