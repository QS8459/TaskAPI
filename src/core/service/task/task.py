from fastapi import Depends;
from src.db.engine import get_async_session;
from sqlalchemy.ext.asyncio import AsyncSession;
from src.core.service.base import AbstractBaseService;
from sqlalchemy.future import select;
from src.db.models.task.task import Task;
from sqlalchemy.exc import SQLAlchemyError;

class TaskService(AbstractBaseService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Task);

    async def add_task(self, user, **kwargs):
        kwargs['created_by'] = user.id;
        return await super().create(**kwargs);

    async def get_all_task(self, user):
        try:
            async with self.session:
                query = select(self.model).where(self.model.created_by == user.id);
                result = await self.session.execute(query);
                return result.scalars().all()
        except SQLAlchemyError as e:
            raise e;


def get_task_service(session: AsyncSession = Depends(get_async_session)) -> AsyncSession:
    return TaskService(session);


