from pydantic import BaseModel;
from pydantic.types import UUID;
from src.db.models.task.task import Status
from src.core.schemas.account import AccountDetail;
class TaskBaseSchema(BaseModel):
    title: str;
    summary: str;
    status: Status;


class TaskCreateSchema(TaskBaseSchema):
    pass;

class TaskUpdateSchema(TaskBaseSchema):
    pass;

class TaskListSchema(TaskBaseSchema):
    id:UUID;
    account: AccountDetail;

class TaskDetailSchema(TaskBaseSchema):
    id:UUID;