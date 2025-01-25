from datetime import datetime
from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing_extensions import Union
from pydantic import ValidationError

from src.db.models import Account
from src.db.engine import get_async_session
from src.core.service.base import BaseService
from src.core.service.account.auth import JWTHasher, reuseable_oauth, jwt
from src.core.schemas.token import TokenSchemaBase


class AccountService(BaseService, JWTHasher):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Account)

    async def before_add(self, **kwargs) -> Union[int, None]:
        email = await self.get_by_email(email=kwargs.get("email"))
        if not email:
            password = kwargs.pop("password")
            self.instance.set_password(password=password)
            return 0
        raise ValueError("Email Already Exists")

    async def get_by_email(self, email) -> Union[Account, None]:
        async def _get_by_email(email=email):
            query = select(self.model).where(self.model.email == email)
            return await self.session.execute(query)

        instance = await self._exe_in_session(_get_by_email, email=email)
        if instance:
            return instance
        return None

    async def auth_user(self, email, password) -> Union[TokenSchemaBase, HTTPException]:
        instance = await self.get_by_email(email)
        if instance:
            verification = instance.verify_password(password)
            if verification:
                access_tkn = JWTHasher.create_access_token(
                    instance.email, expires_delta=30
                )
                refresh_tkn = JWTHasher.create_refresh_token(
                    instance.email, expires_delta=1440
                )

                return TokenSchemaBase(access_tkn=access_tkn, refresh_tkn=refresh_tkn)

        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong login or password",
        )


def account_service(
    session: AsyncSession = Depends(get_async_session),
) -> AccountService:
    return AccountService(session)


async def get_current_account(
    token: str = Depends(reuseable_oauth), service=Depends(account_service)
):
    try:

        payload = jwt.decode(token, "123", algorithms=["HS256"])
        if datetime.fromtimestamp(payload.get("exp")) < datetime.utcnow():
            raise HTTPException(
                detail="Authorization Error",
                status_code=status.HTTP_401_FORBIDDNE,
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            detail="Authorization Error",
            status_code=status.HTTP_403_FORBIDDNE,
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await service.get_by_email(payload.get("sub"))

    return user
