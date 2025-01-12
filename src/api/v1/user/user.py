from uuid import UUID
from fastapi import APIRouter, Depends

from src.core.service.account.account import account_service
from src.core.schemas.account import (
    AccountSignInSchema,
    CustomAuthForm,
    AccountResponseSchema,
)
from src.core.schemas.token import TokenSchemaBase

user_api = APIRouter(prefix="/user")


@user_api.post("/sign_in/")
async def sing_in(data: AccountSignInSchema, service=Depends(account_service)):
    instance = await service.add(**data.dict())
    return instance


@user_api.get("/{id}", status_code=200)
async def get_user(id: UUID, service=Depends(account_service)):
    instance = await service.get_by_id(id=id)
    return instance


@user_api.get("/{email}/")
async def get_user_by_email(email: str, service=Depends(account_service)):
    instance = await service.get_by_email(email)
    return instance


@user_api.post("/login/", response_model=TokenSchemaBase)
async def login(
    form_data: CustomAuthForm = Depends(), service=Depends(account_service)
):
    response = await service.auth_user(form_data.username, form_data.password)
    return response


@user_api.get("/me/", response_model=AccountResponseSchema)
async def me(user: AccountSignInSchema = Depends(account_service().get_current_user)):
    return user
