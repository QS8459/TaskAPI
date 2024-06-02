from fastapi import APIRouter, Depends, HTTPException,status;
from src.core.service.task.task import get_task_service;
from src.core.schema.task import TaskDetail;
router = APIRouter(prefix = "/task", tags = ['task']);

@router.get('/all')
async def get_tasks(
        task_service = Depends(get_task_service)
):
    task = await task_service.get_all();
    return task;

@router.get("/{pk}")
async def get_task_by_id(
        pk:int,
        task_service = Depends(get_task_service)
    ):
    try:
        return await task_service.get_by_id(pk);
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        );

@router.get("/count/get")
async def get_count(
        task_service = Depends(get_task_service)
):
    try:
        return await task_service.get_count();
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        );

@router.put("/{task_id}")
async def update_task(
        task_id: int,
        task_data: dict,
        task_service = Depends(get_task_service)
):
    try:
        task = await task_service.update(task_id, **task_data);
        if task is None:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "Task is not found"
            )
        return task
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "BAD REQUEST"
        )

@router.delete('/{pk}')
async def delete_task(
        pk:int,
        task_service = Depends(get_task_service)
):
    try:
        response = await task_service.delete(pk);
        if response:
            return True
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "BAD REQUEST"
        )
    return False;

@router.post("/create")
async def add_task(
        task_data:dict,
        task_service = Depends(get_task_service)
):
    try:
        requ = await task_service.create(**task_data);
        if requ:
            return True;
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="BAD REQUEST",
        )
    return False;