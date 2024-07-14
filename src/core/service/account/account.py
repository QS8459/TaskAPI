from fastapi import Depends;
from pydantic.types import UUID;

from sqlalchemy.future import select;
from sqlalchemy.exc import SQLAlchemyError;
from sqlalchemy.ext.asyncio import AsyncSession;

from src.ver_email import email_server, Email;

from src.db.models import Account;
from src.db.engine import get_async_session
from src.core.service import AbstractBaseService;
from src.core.schemas.account import AccountLoginSchema;

class AccountService(AbstractBaseService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Account)

    async def add_account(self, **kwargs) -> Account:
        try:
            async with self.session:
                password = kwargs.pop("password")
                instance = self.model(**kwargs);
                instance.set_password(password);
                self.session.add(instance);
                await self.session.commit();
                await self.session.refresh(instance);
                email_server(Email(
                    subject="Verify Your Email",
                    body=f"http://127.0.0.1:8000/api/v1/account/verify_account/{instance.id}/",
                    recipient=instance.email
                ));
                return instance;
        except SQLAlchemyError as e:
            raise e;

    async def get_by_email(self, email:str):
        try:
            async with self.session:
                query = select(self.model).where(self.model.email == email);
                result = await self.session.execute(query);
                instance = result.scalars().first();
                if not instance:
                    raise ValueError(f"{self.model.__name__} not found")
                return instance;
        except SQLAlchemyError as e:
            raise e;

    async def auth_user(self, credential:AccountLoginSchema):
        try:
            async with self.session:
                account = await self.get_by_email(credential.email);
                if not account:
                    raise ValueError(f"{self.model.__name__} not found");
                if not account.verify_password(credential.password):
                    raise ValueError(f"{self.model.__name__} Invalid Password")
                if account.is_active == False:
                    raise ValueError(f"{self.model.__name__} not found")
                return account;
        except SQLAlchemyError as e:
            raise e;

    async def activate_user(self, id_:UUID):
        try:
            async with self.session:
                account = await super().get_and_update(id_, is_active = True);
                if not account:
                    raise ValueError("Something went wrong in", account.__name__);
                return account;
        except SQLAlchemyError as e:
            raise e;

def get_account_service(session:AsyncSession = Depends(get_async_session)) -> AccountService:
    return AccountService(session);