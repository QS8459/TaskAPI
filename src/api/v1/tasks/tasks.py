from fastapi import APIRouter, Depends

from src.core.service.task.task import get_task_service
from src.core.service.account.account import get_current_account
from src.core.schemas.task import TaskBaseSchema, TaskResponseModel

task_api = APIRouter(prefix="/task")


@task_api.post("/add/private/")
async def add_task_private(
    fields: TaskBaseSchema,
    task_service=Depends(get_task_service),
    user=Depends(get_current_account),
):

    return await task_service.add(**fields.dict(), created_by=user.id)


@task_api.post("/add/", response_model=TaskResponseModel, status_code=201)
async def add_task_no_private(
    fields: TaskBaseSchema,
    task_service=Depends(get_task_service),
):
    result = await task_service.add(**fields.dict())
    return result
