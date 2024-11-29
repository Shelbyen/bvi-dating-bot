from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class PhotoModel(Base):
    __tablename__ = "photos"

    id: Mapped[str] = mapped_column(ForeignKey('users.id'), primary_key=True)
    photo_id: Mapped[str] = mapped_column(String, primary_key=True)
