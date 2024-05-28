from pydantic import BaseModel;

class TaskBase(BaseModel):
    description: str;


class AddTask(TaskBase):
    description: str;

class Task(TaskBase):
    id: int;

    class Config:
        orm_mode = True;