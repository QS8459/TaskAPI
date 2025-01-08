from sqlalchemy.orm import Mapped, mapped_column, relationship;
from src.db.models.base import AbsModel;
from passlib.hash import pbkdf2_sha256 as sha256
from typing import List;
class Account(AbsModel):
    __tablename__ = "account";
    email: Mapped[str] = mapped_column(nullable = False, unique = True);
    password: Mapped[str] = mapped_column(nullable = False);
    task: Mapped[List["Task"]] = relationship(back_populates="account", lazy="selectin");
    profile: Mapped['Profile'] = relationship(back_populates='account', lazy = 'selectin')

    def set_password(self, password):
        self.password = sha256.using().hash(password);


    def verify_password(self,password):
        return sha256.verify(password, self.password);

    def to_dict(self):
        return {
            'email':self.email,
        }

__all__ = ("Account")