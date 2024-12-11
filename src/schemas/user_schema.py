from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.photo_schema import PhotoBase
from src.schemas.subjects_schema import SubjectsBase


class UserBase(BaseModel):
    id: str
    name: str
    sex: bool
    priority: Optional[bool]
    town: int
    description: str
    school_class: int
    subjects: SubjectsBase
    photos: list[PhotoBase]
    deactivated: bool = Field(default=False)


class UserCreate(BaseModel):
    id: str
    name: str
    sex: bool
    priority: Optional[bool]
    town: Optional[str]
    description: Optional[str]
    school_class: int


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    pass


class UserListResponse(UserBase):
    pass
