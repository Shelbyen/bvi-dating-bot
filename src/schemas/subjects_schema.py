from typing import Optional

from pydantic import BaseModel, Field


class SubjectsBase(BaseModel):
    id: str
    math: bool
    physics: bool
    astronomy: bool
    computer_science: bool
    geography: bool
    ecology: bool


class SubjectsCreate(BaseModel):
    id: str
    math: bool = Field(default=False)
    physics: bool = Field(default=False)
    astronomy: bool = Field(default=False)
    computer_science: bool = Field(default=False)
    geography: bool = Field(default=False)
    ecology: bool = Field(default=False)


class SubjectsUpdate(SubjectsBase):
    pass


class SubjectsResponse(BaseModel):
    id: str


class SubjectsListResponse(SubjectsBase):
    pass
