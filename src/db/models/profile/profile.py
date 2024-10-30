from src.db.models.base import AbsModel;
from sqlalchemy.orm import mapped_column, Mapped, relationship;
from sqlalchemy import String, ForeignKey;
from datetime import datetime;
from pydantic.types import UUID

class Profile(AbsModel):
    __tablename__ = "profile";
    name: Mapped[str] = mapped_column(String(100), nullable = True);
    age: Mapped[int] = mapped_column(nullable=True, unique = False);
    birth_date: Mapped[datetime] = mapped_column(nullable = True);
    username: Mapped[str] = mapped_column(String(100),nullable = True);
    instagram: Mapped[str] = mapped_column(nullable = True);
    facebook: Mapped[str] = mapped_column(nullable= True);
    account: Mapped["Account"] = relationship(back_populates="profile",lazy = 'joined')
    owner: Mapped[UUID] = mapped_column(ForeignKey('account.id'));
    is_active: Mapped[bool] = mapped_column(default = True);
    about: Mapped[str] = mapped_column(String(500), nullable = True);




__all__ = ("Profile");


