from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: str
    name: str
    sex: bool
    priority: Optional[bool]
    town: int
    description: str
    school_class: int
    media_count: int


class UserCreate(BaseModel):
    id: str
    name: str
    sex: bool
    priority: Optional[bool]
    town: Optional[str]
    description: Optional[str]
    school_class: int
    media_count: int = Field(default=0)


class UserUpdate(UserBase):
    pass


class UserResponse(BaseModel):
    pass


class UserListResponse(UserBase):
    pass
