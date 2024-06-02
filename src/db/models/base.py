from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped;
from datetime import datetime
class AbstractModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(autoincrement=True, nullable= False, primary_key= True)
    created_at:Mapped[datetime] = mapped_column(default=datetime.utcnow);
    updated_at:Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow);
    is_active: Mapped[bool] = mapped_column(default = True)
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"