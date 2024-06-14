import jwt
from typing import Annotated
from src.config import settings
from datetime import datetime, timedelta;
from src.core.schemas.account import Token, AccountDetail, AccountBaseSchema;
from src.db.engine import get_async_session;
from sqlalchemy.ext.asyncio import AsyncSession;
from fastapi import Depends, status, HTTPException;
from src.core.service.account.account import get_account_service;
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm;

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "/api/v1/account/login/")
def generate_access_token(data: dict,   expiration_delta: timedelta | None = None)->Token:
    to_encode = data.copy();
    if expiration_delta:
        expire = datetime.utcnow() + expiration_delta;
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15);
    to_encode.update({"exp":expire});
    encoded_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm =settings.algorithm);
    return Token(token = encoded_jwt, type = 'bearer');

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]= None, account_service = Depends(get_account_service)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm]);
        email:str = payload.get('sub');
        if email is None:
            raise credentials_exception
        token_data = AccountBaseSchema(email=email);
    except Exception as e:
        raise credentials_exception
    user = await account_service.get_by_email(token_data.email);
    if user is None:
        raise credentials_exception;
    return user;

async def get_current_active_user(
        current_user: Annotated[AccountDetail, Depends(get_current_user)]
):
    if current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = "Inactive User");
    return current_user;


