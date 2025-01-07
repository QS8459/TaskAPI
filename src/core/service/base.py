from typing import Generic, TypeVar, Type;
from sqlalchemy.ext.asyncio import AsyncSession;
from sqlalchemy.exc import SQLAlchemyError, IntegrityError;
from sqlalchemy.future import select
from abc import ABC, abstractmethod;
from uuid import UUID;
T = TypeVar("T");

class BaseService(ABC, Generic[T]):
    def __init__(self, session: AsyncSession, model:Type[T]):
        self.session = session;
        self.model = model;

    async def __commit_in_session(self, callable, refresh = True,*args, **kwargs):
        try:
            result = await callable(*args,**kwargs)
            await self.session.commit();
            if result and refresh:
                await self.session.refresh();
            return result;
        except SQLAlchemyError as e:
            raise SQLAlchemyError(e);
        except IntegrityError as e:
            raise IntegrityError(e);
        except Exception as e:
            raise Exception(e);

    async def __exe_in_session(self, query):
        try:
            result = await self.session.execute(query);
            return result.scalars().first();
        except IntegrityError as e:
            raise IntegrityError(e);
        except SQLAlchemyError as e:
            raise SQLAlchemyError(e);
        except Exception as e:
            raise Exception(e);

    @abstractmethod
    def before_add(self,*args, **kwargs):
        pass
    async def add(self, *args, **kwargs) -> T:
        async def _add(**kwargs):
            instance = self.model(**kwargs)
            self.before_add(**kwargs)
            self.session.add(instance)
            return instance
        instance = await self.__commit_in_session(_add, **kwargs)
        return instance

    async def get_by_id(self, id: UUID) -> T:
        query = select(self.model).where(self.model.id == id)
        instance = self.__exe_in_session(query)
        if not instance:
            return None
        return instance

    async def update(self, id: UUID, **kwargs) -> T:
        async def _update(id:UUID):
            instance = await self.get_by_id(id);
            for k,v in kwargs.items():
                setattr(instance,k,v)
            self.session.add(instance)
            return instance
        instance = await self.__commit_in_session(_update, refresh = False, **kwargs)

        return instance