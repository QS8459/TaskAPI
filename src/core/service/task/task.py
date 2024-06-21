from fastapi import Depends;
from src.db.engine import get_async_session;
from sqlalchemy.ext.asyncio import AsyncSession;
from src.core.service.base import AbstractBaseService;

from src.db.models.task.task import Task;

class TaskService(AbstractBaseService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Task);

    async def add_task(self, user, **kwargs):
        kwargs['created_by'] = user.id;
        return await super().create(**kwargs);

def get_task_service(session: AsyncSession = Depends(get_async_session)) -> AsyncSession:
    return TaskService(session);


