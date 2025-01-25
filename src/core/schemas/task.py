from pydantic import BaseModel
from uuid import UUID
from typing_extensions import Annotated, Doc
from fastapi.param_functions import Form
from enum import Enum


class Status(str, Enum):
    PENDING: str = "PENDING"
    ONGOING: str = "ONGOING"
    CANCELED: str = "CANCELED"
    DONE: str = "DONE"
    ARCHIVED: str = "ARCHIVED"


class TaskBaseSchema(BaseModel):
    title: Annotated[
        str,
        Form(),
        Doc(
            """
            title field takes string
            """
        ),
    ]
    summary: Annotated[
        str,
        Form(),
        Doc(
            """
            summary field takes string
            """
        ),
    ]
    status: Annotated[
        Status,
        Form(),
        Doc(
            """
            status
            """
        ),
    ]


class TaskResponseModel(TaskBaseSchema):
    id: UUID
