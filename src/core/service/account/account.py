from fastapi import Depends;
from pydantic.types import UUID;

from sqlalchemy.future import select;
from sqlalchemy.exc import SQLAlchemyError;
from sqlalchemy.ext.asyncio import AsyncSession;

from src.ver_email import email_server, Email;

from src.db.models import Account;
from src.db.engine import get_async_session
from src.core.service.base import BaseService;
from src.core.schemas.account import AccountLoginSchema;

class AccountService(BaseService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Account)


def get_account_service(session:AsyncSession = Depends(get_async_session)) -> AccountService:
    return AccountService(session);