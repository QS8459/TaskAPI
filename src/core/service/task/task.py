from typing import Annotated;

from fastapi import Depends;
from src.db.engine import get_async_session;
from sqlalchemy.ext.asyncio import AsyncSession;
from src.core.service.base import BaseService;
from sqlalchemy.future import select;
from src.db.models.task.task import Task;
from sqlalchemy.exc import SQLAlchemyError;
from sqlalchemy import func, asc, desc;

from src.core.schemas.account import AccountDetail;
from src.pagination import Pagination, pagination_param

class TaskService(BaseService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Task);


def get_task_service(session: AsyncSession = Depends(get_async_session)) -> AsyncSession:
    return TaskService(session);


