from src.services.base_service import BaseService
from ..repositories.photo_repository import photo_repository
from ..schemas.photo_schema import PhotoCreate


class PhotoService(BaseService):
    async def create_many(self, photos: list[PhotoCreate]) -> None:
        if len(photos) != 0:
            await self.repository.create_many(photos)

photo_service = PhotoService(repository=photo_repository)