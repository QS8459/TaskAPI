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
        instance = await self.__commit_in_session(_update, refresh = False, id = id, **kwargs)

        return instance

    async def hard_delete(self, id: UUID) -> str:
        async def _delete(id: UUID):
            instance = await self.get_by_id(id);
            await self.session.delete(instance);
            return instance

        instance = await self.__commit_in_session(_delete, refresh = False, id = id)

    async def filter(self, fields=None, **kwargs):
        """
        Filter records with dynamic criteria and select specific columns.

        Args:
            fields (list): List of fields to retrieve. If None, retrieves all columns.
                           Example: fields=["id", "name"]
            kwargs: Key-value pairs for filtering.
                    Example: filter(name="Alice", age=30)

        Returns:
            List of filtered results (as dictionaries if fields are specified) or None in case of error.
        """
        query = select(self.model)

        if fields:
            selected_fields = [getattr(self.model, field) for field in fields if hasattr(self.model, field)]
            if not selected_fields:
                raise AttributeError("No valid fields specified for selection.")
            query = select(*selected_fields)

        for field, value in kwargs.items():
            if hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
            else:
                raise AttributeError(f"Field '{field}' does not exist in model '{self.model.__name__}'.")

        response = await self.__exe_in_session(query)

        if not response:
            return None
        return response