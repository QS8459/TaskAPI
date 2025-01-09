from fastapi import Depends;
from sqlalchemy.ext.asyncio import AsyncSession;
from sqlalchemy.future import select
from src.db.models import Account;
from src.db.engine import get_async_session
from src.core.service.base import BaseService;

class AccountService(BaseService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Account)

    async def before_add(self, instance=None, **kwargs):
        email = await self.get_by_email(email = kwargs.get('email'))
        if not email:
            password = kwargs.pop('password')
            instance.set_password(password=password)
            return 0
        raise ValueError("Email Already Exists")



    async def get_by_email(self, email):
        query = select(self.model).where(self.model.email == email)
        instance = await self._exe_in_session(query, fetch_one= True)
        return instance


def account_service(session: AsyncSession = Depends(get_async_session)) -> AccountService:
    return AccountService(session);