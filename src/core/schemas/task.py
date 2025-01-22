from pydantic import BaseModel
from uuid import UUID


class TaskBaseSchema(BaseModel):
    title: str
    summary: str
    status: str


class TaskResponseModel(TaskBaseSchema):
    id: UUID
