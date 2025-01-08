from src.core.service.account.account import account_service
from fastapi import APIRouter, Depends
from src.core.schemas.account import AccountSchema
from uuid import UUID

user_api = APIRouter(prefix='/user')


@user_api.post('/sign_in/')
async def sing_in(
        data: AccountSchema,
        service=Depends(account_service)
):
    instance = await service.add(**data.dict());
    return instance


@user_api.get('/user/{id}', status_code=200)
async def get_user(
        id: UUID,
        service=Depends(account_service)
):
    instance = await service.get_by_id(id=id)
    return instance


@user_api.get('/users/list/', status_code = 200)
async def get_users(
        id: UUID,
        service = Depends(account_service)
):
    results = await service.filter(id = id)
    return results
