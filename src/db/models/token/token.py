from src.db.models.base import AbsModel;
# from src.db.models.account.account import Account;
from sqlalchemy.orm import Mapped, mapped_column, relationship;
from datetime import datetime, timedelta;
from src.config import settings;
from pydantic.types import UUID
from sqlalchemy import ForeignKey
class Token(AbsModel):
    __tablename__ = "token";
    access: Mapped[str] = mapped_column(nullable = False);
    refresh_token: Mapped[str] = mapped_column(nullable = False);
    expires_at: Mapped[datetime] = mapped_column(default = datetime.utcnow() + timedelta(minutes = settings.token_expiration));
    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.id"));
    account: Mapped["Account"] = relationship(back_populates="token", lazy="selectin")


__all__ = ("Token")
