import jwt

from typing import Union, Any
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from abc import ABC

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/user/login/", scheme_name="jwt"
)


class JWTHasher(ABC):
    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: int = None):
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=30)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, "123", "HS256")
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None):
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=30)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, "123", "HS256")
        return encoded_jwt
