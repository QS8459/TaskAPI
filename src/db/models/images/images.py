from src.db.models.base import AbsModel;
from sqlalchemy.orm import Mapped, mapped_column, relationship;
from pydantic.types import UUID

from sqlalchemy import ForeignKey;

class Images(AbsModel):
    __tablename__ = "images";
    path: Mapped[str] = mapped_column(unique=False);
    owner: Mapped[UUID] = mapped_column(ForeignKey('profile.id'));


__all__ = ('Images');