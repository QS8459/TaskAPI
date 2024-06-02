from fastapi import Depends;
from sqlalchemy.ext.asyncio import AsyncSession;

from src.core.service.base import AbstractBaseService;
from src.db.db import get_async_session;
from src.db.models.task.task import Task;


class TaskService(AbstractBaseService[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Task);


def get_task_service(session: AsyncSession = Depends(get_async_session)):
    return TaskService(session);