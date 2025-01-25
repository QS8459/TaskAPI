from fastapi import Depends
from src.db.engine import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.service.base import BaseService
from src.db.models.task.task import Task


class TaskService(BaseService):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Task)

    async def before_add(self, *args, **kwargs):
        pass


def get_task_service(session: AsyncSession = Depends(get_async_session)) -> TaskService:
    return TaskService(session)
