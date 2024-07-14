from typing import List
from src.core.schemas.task import (
    TaskCreateSchema,
    TaskDetailSchema,
    TaskListSchema,
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
        return task;
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        );

@router.get('/all/',
            response_model = List[TaskListSchema],
            status_code=status.HTTP_200_OK)
async def get_all_task(
        current_user = Depends(get_current_user),
        task_service = Depends(get_task_service)
):
    try:
        tasks = await task_service.get_all_task(current_user);
        return tasks;
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        );
@router.get('/{pk}/',
            status_code= status.HTTP_200_OK,
            response_model = TaskDetailSchema)
async def get_a_task(
        pk,
        # current_user = Depends(get_current_user),
        task_service = Depends(get_task_service),
):
    try:
        task = await task_service.get_by_id(pk);
        return task;
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"{e}"
        )