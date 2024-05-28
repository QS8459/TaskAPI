from fastapi import APIRouter, Depends, HTTPException, Body;
from sqlalchemy.orm import Session;
from . import crud;
from typing import List;
from src.models.task import Task;
from src.schemas import task;
from src.db.engine import get_db;

router = APIRouter();

@router.get('/list/', response_model = List[task.Task])
async def todo_list(skip:int = 0,limit:int = 10,db:Session = Depends(get_db)) -> List[Task]:
    tasks = crud.get_tasks(db=db, skip = skip, limit = limit);
    return tasks;

@router.post('/add/')
async def add_todo(task: task.AddTask = Body(...), db:Session = Depends(get_db)):
    return crud.add_task(db = db, task = task);

@router.get('/{task_id}/')
async def post_detail(task_id:int, db:Session = Depends(get_db)):
    db_task = crud.get_task(db = db, task_id= task_id);
    if db_task == None:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return db_task

