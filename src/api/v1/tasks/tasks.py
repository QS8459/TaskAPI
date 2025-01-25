from fastapi import APIRouter, Depends

from src.core.service.task.task import get_task_service
from src.core.service.account.account import get_current_account
from src.core.schemas.task import (
    TaskBaseSchema,
    TaskResponseModel,
    TaskListModelReponse,
)

# from typing_extensions import List
from uuid import UUID
from src.logger import log

task_api = APIRouter(prefix="/task", tags=["task"])


@task_api.post("/add/", response_model=TaskResponseModel)
async def add_task(
    fields: TaskBaseSchema,
    user=Depends(get_current_account),
    task_service=Depends(get_task_service),
):

    return await task_service.add(**fields.dict(), created_by=user.id)


@task_api.put("/update/{id}/", response_model=TaskResponseModel)
async def update_task(
    id: UUID,
    fields: TaskBaseSchema,
    user=Depends(get_current_account),
    task_service=Depends(get_task_service),
):
    return await task_service.update(id, **fields.dict())


@task_api.get("/list/", response_model=TaskListModelReponse(TaskResponseModel))
async def task_list(
    user=Depends(get_current_account), task_service=Depends(get_task_service)
):
    result = await task_service.filter(created_by=user.id)
    log.error(f"This is result form /task/list api {result}")
    return {"data": result}
