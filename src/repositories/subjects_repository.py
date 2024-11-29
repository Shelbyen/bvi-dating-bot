from src.repositories.sqlalchemy_repository import SqlAlchemyRepository
from src.models.subjects_model import SubjectsModel
from src.config.database.db_helper import db_helper

from ..schemas.subjects_schema import SubjectsCreate, SubjectsUpdate


class SubjectsRepository(SqlAlchemyRepository[SubjectsModel, SubjectsCreate, SubjectsUpdate]):
    pass


subjects_repository = SubjectsRepository(model=SubjectsModel, db_session=db_helper.get_db_session)
