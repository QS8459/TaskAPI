from src.core.schemas.task import (
    TaskCreateSchema,
    TaskDetailSchema,
);
from src.core.service.task.task import get_task_service
from src.core.service.account.auth import get_current_user;
from fastapi import APIRouter, Depends, HTTPException, status;
router = APIRouter(prefix = '/task', tags = ['task']);

@router.post('/add/',
             status_code = status.HTTP_201_CREATED,
             response_model = TaskDetailSchema)
async def add_task(
    data: TaskCreateSchema,
    current_user = Depends(get_current_user),
    task_service = Depends(get_task_service),
):
    try:
        task = await task_service.add_task(user = current_user, **data.dict());
        print(current_user);
        return task;
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"{e}"
        );

