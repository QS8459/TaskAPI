from src.core.service.account.account import account_service
from fastapi import APIRouter, Depends
from src.core.schemas.account import AccountSchema

user_api = APIRouter(prefix = '/user')

@user_api.post('/sign_in/')
async def sing_in(
        data: AccountSchema,
        service = Depends(account_service)
):
    instance = await account_service().add(**data.dict());
    return instance