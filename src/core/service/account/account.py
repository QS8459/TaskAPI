from fastapi import Depends;
from sqlalchemy.ext.asyncio import AsyncSession;
from src.db.models import Account;
from src.db.engine import get_async_session
from src.core.service.base import BaseService;

class AccountService(BaseService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Account)

    def before_add(self, **kwargs):
        self.model.password = self.model.set_password(kwargs.get('password'))



def account_service(session:AsyncSession = Depends(get_async_session)) -> AccountService:
    return AccountService(session);