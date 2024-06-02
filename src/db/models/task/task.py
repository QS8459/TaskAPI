from sqlalchemy import String;
from sqlalchemy.orm import mapped_column, Mapped;
from src.db.models.base import AbstractModel;
class Task(AbstractModel):
    __tablename__ = "task";
    description:Mapped[str] = mapped_column(String,index = True);

__all__ =(
    "Task"
);