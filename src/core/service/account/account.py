from src.core.service import AbstractBaseService;
from sqlalchemy.ext.asyncio import AsyncSession;
from fastapi import Depends;
from sqlalchemy.exc import SQLAlchemyError;
from src.db.engine import get_async_session
from src.db.models import Account;
from src.core.schemas.account import AccountLoginSchema;
from sqlalchemy.future import select;
class AccountService(AbstractBaseService):
    def __init__(self, session:AsyncSession):
        super().__init__(session, Account)

    async def add_account(self, **kwargs) -> Account:
        try:
            async with self.session:
                password = kwargs.pop("password")
                instance = self.model(**kwargs);
                print(instance);
                instance.set_password(password);
                print("This is it's email",instance.email);
                print("This is it's password", instance.password);
                self.session.add(instance);
                await self.session.commit();
                await self.session.refresh(instance);
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
                return account;
        except SQLAlchemyError as e:
            raise e;

def get_account_service(session:AsyncSession = Depends(get_async_session)) -> AccountService:
    return AccountService(session);