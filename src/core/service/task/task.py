from typing import Annotated;

from fastapi import Depends;
from src.db.engine import get_async_session;
from sqlalchemy.ext.asyncio import AsyncSession;
from src.core.service.base import AbstractBaseService;
from sqlalchemy.future import select;
from src.db.models.task.task import Task;
from sqlalchemy.exc import SQLAlchemyError;
from sqlalchemy import func;

from src.core.schemas.account import AccountDetail;
from src.pagination import Pagination, pagination_param

class TaskService(AbstractBaseService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Task);

    async def add_task(self, user, **kwargs):
        kwargs['created_by'] = user.id;
        return await super().create(**kwargs);

    async def get_all_task(self, user: AccountDetail, pagination: Annotated[Pagination, Depends(pagination_param)]):
        try:
            async with self.session:
                query = (
                    select(self.model).filter(self.model.created_by == user.id)
                    .limit(pagination.perPage)
                    .offset(
                        pagination.page - 1
                        if pagination.page == 1
                        else (pagination.page - 1) * pagination.perPage
                    )
                );

                result = await self.session.execute(query);

                task = result.scalars().all();
                count_query = select(func.count()).select_from(self.model).filter(self.model.created_by == user.id)
                result_c = await self.session.execute(count_query);
                count = result_c.scalar();
                return {'task':task, 'count':count}
        except SQLAlchemyError as e:
            raise e;


def get_task_service(session: AsyncSession = Depends(get_async_session)) -> AsyncSession:
    return TaskService(session);


