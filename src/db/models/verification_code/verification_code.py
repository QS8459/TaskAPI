from sqlalchemy import Integer;
from pydantic.types import UUID;
from src.db.models.base import AbsModel;
from sqlalchemy.orm import relationship;
from datetime import datetime, timedelta;
from sqlalchemy.orm import Mapped, mapped_column;
from sqlalchemy import ForeignKey;
class Verification_Code(AbsModel):
    __tablename__ = "verification_code"
    verification_code:Mapped[int] = mapped_column(Integer, nullable=True);
    active_till: Mapped[datetime] = mapped_column(default = datetime.utcnow() + timedelta(minutes = 2));
    code_for:Mapped[UUID] = mapped_column(ForeignKey('account.id'));
    account: Mapped["Account"] = relationship(back_populates="ver_code",lazy='joined');
    is_active: Mapped[bool] = mapped_column(default=True);
    def verify_code(self,v_code):
        return self.verification_code == v_code;


__all__ = ("verification_code")