from typing import Generic, TypeVar, Type, Tuple, Sequence, Any, Annotated;
from pydantic.types import UUID;

from fastapi import Depends;

from sqlalchemy.ext.asyncio import AsyncSession;
from sqlalchemy import delete, Row, func, update;
from sqlalchemy.exc import SQLAlchemyError;
from sqlalchemy.future import select;

from abc import ABC

from src.pagination import pagination_param, Pagination;
T = TypeVar("T")

class AbstractBaseService(ABC,Generic[T]):
    def __init__(self, session:AsyncSession, model:Type[T]):
        self.session = session;
        self.model = model;

    async def create(self, **kwargs) -> T:
        try:
            async with self.session:
                instance = self.model(**kwargs);
                self.session.add(instance);
                await self.session.commit();
                await self.session.refresh(instance);
                return instance;
        except SQLAlchemyError as e:
            raise e;

    async def get_all(
            self,
            user,
            pagination: Annotated[Pagination, Depends(pagination_param)]
    ):
        try:
            async with self.session:
                query = (
                    select(self.model).filter(self.model.created_by == user.id)
                    .limit(pagination.perPage)
                    .offset(pagination.page - 1
                    if pagination.page == 1
                    else(pagination.page - 1) * pagination.perPage )
                )
                result = await self.session.execute(query);
                return result.scalars().all();
        except SQLAlchemyError as e:
            raise e;

    async def get_by_id(self, _id: UUID) -> T:
        try:
            async with self.session:
                query = select(self.model).where(self.model.id == _id);
                result = await self.session.execute(query);
                instance = result.scalars().first();
                if not instance:
                    raise ValueError(f"{self.model.__name__} not found")
                return instance;
        except SQLAlchemyError as e:
            raise e

    async def get_and_update(self, id_:UUID,**kwargs) -> T:
        try:
            async with self.session:
                instance = await self.get_by_id(id_);
                for k, v in kwargs.items():
                    setattr(instance, k, v);
                self.session.add(instance);
                await self.session.commit();
                await self.session.refresh(instance);
                return instance;
        except SQLAlchemyError as e:
            raise e;

    async def update(self, id_:UUID, **kwargs) -> T:
        try:
            async with self.session:
                instance = self.model(**kwargs)
                update(self.model).where(self.model.id == id_).values(**kwargs);
                await self.session.commit();
                await self.session.refresh(instance);
                return instance;
        except SQLAlchemyError as e:
            raise e;

    async def delete(self, id_:UUID):
        try:
            async with self.session:
                instance = await self.get_by_id(id_);
                await self.session.delete(instance);
                await self.session.commit();
        except SQLAlchemyError as e:
            raise e;


    async def get_all_paginated(
            self,
            page: int = 1,
            page_size: int = 25,
    )-> Tuple[int, Sequence[Row[Any]]]:
        try:
            async with self.session:
                limit = page_size;
                offset = (page-1) * page_size;
                instance = await self.get_all();
                count = await self.get_count();
                return count, instance;
        except SQLAlchemyError as e:
            raise e;

    async def get_count(self) -> int:
        try:
            async with self.session:
                query = select(func.count()).select_from(self.model)
                result = await self.session.execute(query);
                count = result.scalar();
                return count;
        except SQLAlchemyError as e:
            raise e
