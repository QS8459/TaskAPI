from pydantic import BaseModel;

class TaskBaseSchema(BaseModel):

    description: str;


class TaskDetail(TaskBaseSchema):
    pass;