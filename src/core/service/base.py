from abc import ABC;
from typing import Any, Generic, Sequence, Tuple, Type, TypeVar;

from sqlalchemy import Row, delete, func, update;
from sqlalchemy.exc import SQLAlchemyError;
from sqlalchemy.ext.asyncio import AsyncSession;
from sqlalchemy.future import select;

from src.logger import logger;

T = TypeVar("T");

class AbstractBaseService(ABC, Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session;
        self.model = model;


    async def get_all(self) -> Sequence[Row[Any]]:
        query = select(self.model);

        async with self.session:
            try:
                result = await self.session.execute(query);
            except SQLAlchemyError as e:
                print("Error, ", e);
                return [];

            instances = result.scalars().all();

        return instances;

    async def get_by_id(self, id_: int) -> T:
        async with self.session:
            logger.error("Error")
            query = select(self.model).where(self.model.id == id_);
            result = await self.session.execute(query);
            instance = result.scalars().first();
            if not instance:
                raise ValueError(f"{self.model.__name__} not found");
            return instance;

    async def get_count(self):
        async with self.session:
            try:
                query = select(func.count()).select_from(self.model);
                result = await self.session.execute(query);
            except SQLAlchemyError as e:
                return [];
            count = result.scalar();
        return count;

    async def update(self,id_: int, **kwargs):
        async with self.session:
            try:
                query = update(self.model).where(self.model.id == id_).values(**kwargs);
                result = await self.session.execute(query);
                await self.session.commit();
                query_get = select(self.model).where(self.model.id == id_);
                result = await self.session.execute(query_get);
                instance = result.scalars().first();
                await self.session.refresh(instance);
            except SQLAlchemyError as e:
                return [];
            return instance;

    async def delete(self, id_: int):
        async with self.session:
            try:
                query = delete(self.model).where(self.model.id == id_);
                result = await self.session.execute(query);
                commit = await self.session.commit();
                if result == None:
                    return False;
            except SQLAlchemyError as e:
                print(e);
            return True;

    async def create(self, **kwargs) -> T:
        async with self.session:
            try:
                instance = self.model(**kwargs);
                self.session.add(instance);
                await self.session.commit();
                await self.session.refresh(instance);
                return instance;
            except SQLAlchemyError as e:
                print(e);
                return [];
