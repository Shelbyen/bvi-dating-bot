from typing import Optional

from sqlalchemy import select, func

from src.config.database.db_helper import db_helper
from src.models.user_model import UserModel
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository
from ..schemas.user_schema import UserCreate, UserUpdate


class UserRepository(SqlAlchemyRepository[UserModel, UserCreate, UserUpdate]):
    async def get_random(self) -> Optional[UserModel] | None:
        async with self._session_factory() as session:
            result = (await session.execute(select(self.model).order_by(func.random()))).first()
            if len(result) == 0:
                return None
            return result[0]

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None


user_repository = UserRepository(model=UserModel, db_session=db_helper.get_db_session)
