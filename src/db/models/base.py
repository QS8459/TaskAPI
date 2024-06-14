from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column;
from uuid import uuid4;
from datetime import datetime;
from pydantic.types import UUID
class AbsModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default = uuid4(), nullable = False);
    created_at: Mapped[datetime] = mapped_column(default = datetime.utcnow());
    updated_at: Mapped[datetime] = mapped_column(default = datetime.utcnow(), onupdate=datetime.utcnow());
    is_active: Mapped[bool] = mapped_column(default = False);

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>";

    def __str__(self):
        return f"{self.__class__.__name__}(id = {self.id})";