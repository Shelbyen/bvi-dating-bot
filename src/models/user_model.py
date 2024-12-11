from sqlalchemy import String, Boolean, Text, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from .photo_model import PhotoModel
from .subjects_model import SubjectsModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    sex: Mapped[bool] = mapped_column(Boolean)
    priority: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)
    town: Mapped[str] = mapped_column(String, default='Москва')
    description: Mapped[str] = mapped_column(Text, default='')
    school_class: Mapped[int] = mapped_column(SmallInteger)
    subjects = relationship(
        "SubjectsModel",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan",
        single_parent=True,
        backref="user",
        passive_deletes=True
    )
    photos: Mapped[list["PhotoModel"]] = relationship(
        "PhotoModel",
        uselist=True,
        lazy="joined",
        cascade="all, delete-orphan"
    )
    deactivated: Mapped[bool] = mapped_column(Boolean, default=False)
