from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Enum
from src.db.models.base import AbsModel
from pydantic.types import UUID
from src.db.models.account.account import Account
import enum


class Status(enum.Enum):
    PENDING: str = "PENDING"
    ONGOING: str = "ONGOING"
    CANCELED: str = "CANCELED"
    DONE: str = "DONE"
    ARCHIVED: str = "ARCHIVED"


class Task(AbsModel):
    __tablename__ = "task"
    title: Mapped[str] = mapped_column(String(50))
    summary: Mapped[str] = mapped_column(String(150))
    created_by: Mapped[UUID] = mapped_column(ForeignKey("account.id"), nullable=True)
    account: Mapped["Account"] = relationship(back_populates="task", lazy="joined")
    status: Mapped[str] = mapped_column(Enum(Status), default=Status.PENDING)
    is_active: Mapped[bool] = mapped_column(default=True)


__all__ = (
    "Task",
    "Status",
)
