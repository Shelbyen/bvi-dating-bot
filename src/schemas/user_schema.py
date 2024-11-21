from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    id: str
    name: str
    sex: bool
    priority: bool
    town: int
    description: str
    school_class: int


class UserCreate(BaseModel):
    id: str
    name: str
    sex: bool
    priority: bool
    town: Optional[str]
    description: Optional[str]
    school_class: int


class UserUpdate(UserBase):
    pass


class UserResponse(BaseModel):
    pass


class UserListResponse(UserBase):
    pass
