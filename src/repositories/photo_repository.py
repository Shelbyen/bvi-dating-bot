from sqlalchemy import insert

from src.repositories.sqlalchemy_repository import SqlAlchemyRepository
from src.models.photo_model import PhotoModel
from src.config.database.db_helper import db_helper

from ..schemas.photo_schema import PhotoCreate, PhotoUpdate


class PhotoRepository(SqlAlchemyRepository[PhotoModel, PhotoCreate, PhotoUpdate]):
    async def create_many(self, photos: list[PhotoCreate]) -> None:
        async with self._session_factory() as session:
            await session.execute(
                insert(self.model),
                photos,
            )
            await session.commit()


photo_repository = PhotoRepository(model=PhotoModel, db_session=db_helper.get_db_session)
