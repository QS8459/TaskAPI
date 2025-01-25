from pydantic import BaseModel, create_model as create_pydantic_model
from uuid import UUID
from typing_extensions import Annotated, Doc, List
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


class TaskListModelReponse(BaseModel):

    def __new__(cls, data_model=None):
        if hasattr(data_model, __name__):
            data_model_name = data_model.__name__
        else:
            data_model_name = "???"
        return create_pydantic_model(
            data_model_name + "ListResponse",
            data=(List[data_model], ...),
            __base__=BaseModel,
        )
