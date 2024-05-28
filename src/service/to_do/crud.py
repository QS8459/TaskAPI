from sqlalchemy.orm import Session
from src.models.task import Task;
from src.schemas import task;

def get_task(db:Session,task_id:int):
    return db.query(Task).filter(Task.id == task_id).first();

def get_tasks(db:Session, skip:int = 0, limit:int = 10):
    return db.query(Task).offset(skip).limit(limit).all();

def add_task(db:Session, task: task.AddTask):
    db_task = Task(description=task.description);
    db.add(db_task);
    db.commit();
    db.refresh(db_task);
    return db_task;