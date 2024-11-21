from src.services.base_service import BaseService
from ..repositories.subjects_repository import subjects_repository


class SubjectsService(BaseService):
    pass


subjects_service = SubjectsService(repository=subjects_repository)