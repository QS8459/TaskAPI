from pydantic import BaseModel
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.param_functions import Form
from typing_extensions import Annotated, Doc


class AccountSchemaBase(BaseModel):
    email: str;


class AccountSignInSchema(AccountSchemaBase):
    password: str;

class AccountResponseSchema(AccountSchemaBase):
    id: UUID

class CustomAuthForm(OAuth2PasswordRequestForm):
    def __init__(self, email: Annotated [
        str,
        Form(),
        Doc(
            """
            `email`, string the Custom Oauth2 spec requires the exact field name
            `email`.
            """
        )

    ], password: Annotated[
        str,
        Form(),
        Doc(
            """
            `password` string the Custom Oauth2 spec requires the exact field name
            `password`.
            """
        )
    ]):
        super().__init__(username = email, password = password)


