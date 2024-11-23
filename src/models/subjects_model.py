from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from src.models.user_model import UserModel
from .base_model import Base


class SubjectsModel(Base):
    __tablename__ = "subjects"

    id: Mapped[str] = mapped_column(ForeignKey('users.id'), primary_key=True)
    math: Mapped[bool] = mapped_column(Boolean, default=False)
    physics: Mapped[bool] = mapped_column(Boolean, default=False)
    astronomy: Mapped[bool] = mapped_column(Boolean, default=False)
    computer_science: Mapped[bool] = mapped_column(Boolean, default=False)
    geography: Mapped[bool] = mapped_column(Boolean, default=False)
    ecology: Mapped[bool] = mapped_column(Boolean, default=False)
    # user: Mapped["UserModel"] = relationship(
    #     "UserModel",
    #     back_populates="subjects",
    #     uselist=False
    # )
