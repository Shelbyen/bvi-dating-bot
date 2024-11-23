from sqlalchemy import String, Boolean, Text, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
# from .subjects_model import SubjectsModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    sex: Mapped[bool] = mapped_column(Boolean)
    priority: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)
    town: Mapped[str] = mapped_column(String, default='Москва')
    description: Mapped[str] = mapped_column(Text, default='')
    school_class: Mapped[int] = mapped_column(SmallInteger)
    media_count: Mapped[int] = mapped_column(SmallInteger, default=0)
    # subjects: Mapped["SubjectsModel"] = relationship(
    #     "SubjectsModel",
    #     back_populates="user",
    #     uselist=False,
    #     lazy="joined"
    # )